import re
from datetime import datetime
from typing import List, AsyncIterable, Optional

import dateparser
import pytz
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from dateutil.relativedelta import relativedelta

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class VeraParser(Parser):
    def do_parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, features="html.parser")
        events = soup.find_all("div", {"class": "event-wrapper"})

        return [VeraParser._transform(parsing_context.venue, tag, parsing_context) for tag in events]

    @staticmethod
    def _add_sup_text_from_text(parent_tag: Tag, text: str) -> str:
        sup = parent_tag.find("sup")
        return f"{text} ({sup.text})" if ParserUtil.has_non_empty_text(sup) else text

    @staticmethod
    def _find_extra(tag: Tag) -> str:
        extra_tag = tag.find("h4", {"class": "extra"})
        if extra_tag is None:
            return ""
        extra = ParserUtil.remove_children_text_from(extra_tag, extra_tag.text)
        extra = VeraParser._add_sup_text_from_text(extra_tag, extra)
        return ParserUtil.sanitize_text(extra)

    @staticmethod
    def _transform(venue: Venue, tag: Tag, parsing_context: ParsingContext) -> Event:
        parsing_context.currently_parsing = tag
        source = venue.source_url
        vera_url = tag.find("a", {"class": "event-link"})["href"]
        artist_tag = tag.find("h3", {"class": re.compile(r"artist|artist ")})
        if artist_tag is not None:
            artist = ParserUtil.remove_children_text_from(artist_tag, artist_tag.text)
            artist = VeraParser._add_sup_text_from_text(artist_tag, artist)
            artist = ParserUtil.sanitize_text(artist)
        else:
            artist = vera_url

        extra = VeraParser._find_extra(tag)

        extra_title = tag.find("h4", {"class": "pretitle"})
        if extra_title is not None:
            extra_title = f"({ParserUtil.sanitize_text(extra_title.text)})"
        else:
            extra_title = ""

        when_tag = tag.find("div", {"class": "date"})
        if when_tag is not None:
            when = ParserUtil.remove_children_text_from(when_tag, when_tag.text)
            when = ParserUtil.sanitize_text(when)
            when_time = tag.find("div", {"class": "schedule"}).text
            when_time = when_time[when_time.find("start: ") + 7 : when_time.find("start: ") + 12]
            when_date: Optional[datetime] = dateparser.parse(
                f"{when} {when_time}",
                languages=["nl"],
                settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True},
            )
            if when_date is not None and when_date < (
                datetime.now(pytz.timezone(venue.timezone)) - relativedelta(days=100)
            ):
                when_date = when_date + relativedelta(years=1)
        image_url = tag.find("div", {"class": "artist-image"})["style"]
        image_url_end = image_url.find("'", image_url.find("https") + 4)
        image_url = image_url[image_url.find("https") : image_url_end]

        when_date = when_date if when_date is not None else datetime.now(pytz.timezone(venue.timezone))

        return Event(
            url=vera_url,
            title=f"{artist} {extra_title}".strip(),
            description=f'{artist}{" with support" if extra != "" else ""} {extra}'.strip(),
            venue=venue,
            source=source,
            date_published=datetime.now(),
            when=when_date,
            image_url=image_url,
        )


class VeraProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = VeraProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return VeraSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="vera-groningen",
            name="VERA-Groningen",
            short_name="Vera NL-GRN",
            phone="+31 (0)50 313 46 81",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@vera-groningen.nl",
            source_url="https://www.vera-groningen.nl/programma/",
            url="https://www.vera-groningen.nl",
        )


class VeraSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.vera-groningen.nl/wp/wp-admin/admin-ajax.php?"
        "action=renderProgramme&category=all&page={}&perpage=20&lang=nl",
    ):
        super().__init__(venue, scrape_url, VeraParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=20)
