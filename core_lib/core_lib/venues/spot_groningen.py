from datetime import datetime
from typing import List, AsyncIterable

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from pytz import timezone

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class SpotParser(Parser):
    dateformat: str = "%Y-%m-%dT:%H%M:%S%z"

    def do_parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, "html.parser")
        program_items = soup.find_all("article")
        return [SpotParser._transform(parsing_context.venue, f, parsing_context) for f in program_items]

    @staticmethod
    def _transform(venue: Venue, article: Tag, parsing_context: ParsingContext) -> Event:
        parsing_context.currently_parsing = article
        source = venue.source_url
        base_url = venue.url
        url = article.a.get("href")
        content = article.find("div", {"class": "program__content"})
        figure = article.find("figure").img.get("data-src") if article.find("figure").img else None
        date = datetime.fromtimestamp(int(article["data-datetime"]), tz=timezone(venue.timezone))
        title = content.h1
        content_title = (
            title.text
            if title.find("span") is None
            else title.text.replace(title.span.text, "") + " - " + title.span.text
        )
        description = ParserUtil.stripped_text_or_default_if_empty(content.p, content_title)

        return Event(
            url=url,
            title=content_title,
            description=description,
            venue=venue,
            image_url=f"{base_url}{figure}",
            source=source,
            date_published=datetime.now(),
            when=date,
        )


class SpotProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SpotProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return SpotSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="spot-groningen",
            name="SPOT",
            short_name="Spot NL-GRN",
            phone="+31 (0)50-3680111",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@spotgroningen.nl",
            url="https://www.spotgroningen.nl",
            source_url="https://www.spotgroningen.nl/programma",
        )


class SpotSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.spotgroningen.nl/programma"):
        super().__init__(venue, scrape_url, SpotParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
