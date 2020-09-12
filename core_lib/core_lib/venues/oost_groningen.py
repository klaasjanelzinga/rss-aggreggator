from datetime import datetime
from typing import List, AsyncIterable

import dateparser
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class OostGroningenParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, features="html.parser")
        events = soup.find_all("div", {"class": "agenda-item"})

        return [OostGroningenParser._transform(parsing_context.venue, tag) for tag in events]

    @staticmethod
    def _transform(venue: Venue, tag: Tag) -> Event:
        when_text = tag.find("span", {"class": "agenda-date"}).text
        when_text = when_text.replace("\n", "").strip()
        when_text = when_text[0 : when_text.find("/")].strip()

        when_datetime = dateparser.parse(
            f"{when_text}",
            languages=["nl"],
            settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True},
        )
        title = tag.find("h3", {"class": "agenda-title"}).text
        description_tag = tag.find("span", {"class": "small"})
        description = description_tag.text if description_tag is not None else title
        oost_url = tag.find("a", {"class": "item-link"}).get("href")
        image_url = f'{venue.url}/{tag.find("img").get("src")}'

        return Event(
            url=oost_url,
            title=f"{title}",
            description=description,
            venue=venue,
            source=venue.source_url,
            date_published=datetime.now(),
            when=when_datetime,
            image_url=image_url,
        )


class OostGroningenProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = OostGroningenProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return OostGroningenSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="oost-groningen",
            short_name="Oost NL-GRN",
            name="Oost Groningen",
            phone="",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@komoost.nl",
            url="https://www.komoost.nl",
            source_url="https://www.komoost.nl",
        )


class OostGroningenSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.komoost.nl"):
        super().__init__(venue, scrape_url, OostGroningenParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
