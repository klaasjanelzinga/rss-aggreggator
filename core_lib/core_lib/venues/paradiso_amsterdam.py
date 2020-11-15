import json
from datetime import datetime
from typing import List, Dict, AsyncIterable

import dateparser
import pytz
from aiohttp import ClientSession

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.processing_chain import DatabaseSink, Chain
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class ParadisoParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        program_items = json.loads(parsing_context.content)
        return [ParadisoParser._transform(parsing_context.venue, item) for item in program_items]

    @staticmethod
    def _transform(venue: Venue, data: Dict) -> Event:
        source = venue.source_url
        paradiso_url = f'https://api.paradiso.nl/api/library/lists/events/{data["id"]}?lang=en'
        title = data["title"]
        description = data["subtitle"]
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["start_date_time"]}'

        when = dateparser.parse(
            when_format, languages=["en"], settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True}
        ) or datetime.now(tz=pytz.timezone(venue.timezone))

        return Event(
            url=paradiso_url,
            title=title,
            description=description,
            date_published=datetime.now(),
            venue=venue,
            source=source,
            when=when,
        )

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        additional_json = json.loads(additional_details)
        if len(additional_json) > 0:
            if "content" in additional_json[0]:
                if "alternate_urls" in additional_json[0]["content"]:
                    event.url = additional_json[0]["content"]["alternate_urls"]["en"]
                if "main_image__focus_events" in additional_json[0]["content"]:
                    main_image = additional_json[0]["content"]["main_image__focus_events"]
                    folder_path = main_image["folder_path"]
                    filename = main_image["filename"]
                    event.image_url = f"https://api.paradiso.nl/{folder_path}/{filename}"
        return event


class ParadisoProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = ParadisoProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return ParadisoSource(self.venue)

    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return super().processing_chain_with_additionals(client_session, database_sink)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="paradiso-amsterdam",
            short_name="Paradiso NL-AMS",
            name="Paradiso Amsterdam",
            phone="",
            city="Amsterdam",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@paradiso.nl",
            url="https://www.paradiso.nl",
            source_url="https://www.paradiso.nl/",
        )


class ParadisoSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://api.paradiso.nl/api/events"
        "?lang=en&start_time=now&sort=date&order=asc&limit=30&page={}&with=locations",
    ):
        super().__init__(venue, scrape_url, ParadisoParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=30)
