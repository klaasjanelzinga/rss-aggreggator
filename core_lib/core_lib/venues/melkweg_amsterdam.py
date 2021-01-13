import json
from datetime import datetime
from typing import Dict, List, AsyncIterable

import pytz
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class MelkwegParser(Parser):
    @staticmethod
    def _make_description(event: Dict) -> str:
        description_item = event["description"]
        return (
            BeautifulSoup(description_item, features="html.parser").text
            if description_item is not None
            else event["name"]
        )

    def do_parse(self, parsing_context: ParsingContext) -> List[Event]:
        venue = parsing_context.venue
        source = venue.source_url
        content = json.loads(parsing_context.content)

        results = []
        for day in content:
            events = [event for event in day["events"] if event["type"] == "event"]
            for event in events:
                parsing_context.currently_parsing = event
                description = MelkwegParser._make_description(event)
                date = datetime.fromtimestamp(int(event["date"]), pytz.timezone(venue.timezone))
                title = event["name"]
                image_url = (
                    f"https://s3-eu-west-1.amazonaws.com/static.melkweg.nl/uploads/images/"
                    f'scaled/agenda_thumbnail/{event["thumbnail"]}'
                )
                url = f'https://www.melkweg.nl/nl/agenda/{event["slug"]}'
                results.append(
                    Event(
                        url=url,
                        title=title,
                        description=ParserUtil.sanitize_text(description[:1400]),
                        venue=venue,
                        source=source,
                        date_published=datetime.now(),
                        when=date,
                        image_url=image_url,
                    )
                )
        return results


class MelkwegProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = MelkwegProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return MelkwegSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="melkweg-amsterdam",
            short_name="Melkweg NL-AMS",
            name="Melkweg Amsterdam",
            phone="",
            city="Amsterdam",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@melkweg.nl",
            source_url="https://www.melkweg.nl/agenda",
            url="https://www.melkweg.nl",
        )


class MelkwegSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.melkweg.nl/nl/agenda/as_json/1/grouped/0/page_size/-1?cb=2603211",
    ):
        super().__init__(venue, scrape_url, MelkwegParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
