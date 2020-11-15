from datetime import datetime
from typing import List, AsyncIterable

import dateparser
import pytz
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class SimplonParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, features="html.parser")
        events = soup.find_all("a", {"class": "item"})

        return [SimplonParser._transform(parsing_context.venue, tag) for tag in events]

    @staticmethod
    def _transform(venue: Venue, tag: Tag) -> Event:
        simplon_url = tag.get("href")
        title = tag.get("title")
        subtitle_tag = tag.find("div", {"class": "subtitle"})
        details_tag = tag.find("div", {"class": "details"})
        description = subtitle_tag.text if subtitle_tag is not None else details_tag.text
        when = tag.find("div", {"class": "date"}).text
        time = details_tag.text
        time = time[time.find("Aanvang: ") + 9 : time.find("Aanvang: ") + 15]

        when_datetime = dateparser.parse(
            f"{when} {time}", settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True}
        ) or datetime.now(tz=pytz.timezone(venue.timezone))
        image_url_style = tag.find("div", {"class": "item-image"}).get("style")
        image_url_start = image_url_style.find("https")
        image_url = image_url_style[image_url_start : image_url_style.find(".jpg") + 4]
        return Event(
            url=simplon_url,
            title=f"{title}",
            description=description,
            venue=venue,
            source=venue.url,
            date_published=datetime.now(),
            when=when_datetime,
            image_url=image_url,
        )


class SimplonProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SimplonProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return SimplonSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="simplon-groningen",
            name="Simplon Groningen",
            short_name="Simplon NL-GRN",
            phone="0503184150",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@simplon.nl",
            source_url="https://www.simplon.nl/agenda",
            url="https://www.simplon.nl",
        )


class SimplonSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.simplon.nl"):
        super().__init__(venue, scrape_url, SimplonParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
