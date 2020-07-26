import json
from datetime import datetime
from typing import List, Dict, AsyncIterable

import dateparser
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class T013Parser(Parser):
    dateformat: str = "%Y-%m-%dT:%H%M:%S%z"

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, "html.parser")
        program_items = soup.find("body").find_all_next("script")
        data_script = [p for p in program_items if "src" not in p][0].string
        start_index = data_script.find("event_index:") + 12
        end_index = data_script.find("""]},""") + 2
        json_script = data_script[start_index:end_index]
        json_script = json_script.replace("\\n", "").replace("""\\""", "")
        json_data_events = json.loads(json_script)
        return [T013Parser._transform(parsing_context.venue, json_data) for json_data in json_data_events["events"]]

    @staticmethod
    def _transform(venue: Venue, json_event: Dict) -> Event:
        title = json_event["title"]
        description = json_event["subtitle"]
        if not description:
            description = title
        if "supportAct" in json_event and not json_event["supportAct"] is None:
            title = f"{title} {json_event['supportAct']}"
        source = venue.source_url
        url = f"{venue.url}{json_event['url']}"
        starts_at = json_event["dates"]["startsAt"]
        date = dateparser.parse(starts_at, settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True})
        image_url = f"{venue.url}{json_event['images']['regular']['mobile']}"
        return Event(
            url=url,
            title=title,
            venue=venue,
            image_url=image_url,
            source=source,
            description=description,
            date_published=datetime.now(),
            when=date,
        )


class T013Processor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = T013Processor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return T013Source(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="013-tilburg",
            name="013 Tilburg",
            short_name="013 NL-TIL",
            phone="+31 (0)13-4609500",
            city="Tilburg",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@013.nl",
            url="https://www.013.nl",
            source_url="https://www.013.nl/programma",
        )


class T013Source(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.013.nl/programma"):
        super().__init__(venue, scrape_url, T013Parser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
