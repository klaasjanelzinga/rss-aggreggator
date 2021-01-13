import json
from datetime import datetime
from typing import List, Dict, AsyncIterable

import dateparser
import pytz
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.processing_chain import DatabaseSink, Chain
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class TivoliParser(Parser):
    def do_parse(self, parsing_context: ParsingContext) -> List[Event]:
        program_items = json.loads(parsing_context.content)
        return [TivoliParser._transform(parsing_context.venue, f, parsing_context) for f in program_items]

    @staticmethod
    def _transform(venue: Venue, data: Dict, parsing_context: ParsingContext) -> Event:
        parsing_context.currently_parsing = data
        source = venue.source_url
        tivoli_url = data["link"]
        title = data["title"]
        image_url = data["image"]
        description = data["subtitle"]
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["day"]} {data["month"]} {data["year"]} 00:00'

        when = dateparser.parse(
            when_format, languages=["nl"], settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True}
        ) or datetime.now(tz=pytz.timezone(venue.timezone))

        return Event(
            url=tivoli_url,
            title=title,
            venue=venue,
            image_url=image_url,
            description=description,
            source=source,
            date_published=datetime.now(),
            when=when,
        )

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        soup = BeautifulSoup(additional_details, features="html.parser")
        # find a div with info-inner/label containing a span "aanvang"
        time = None
        for div in soup.find_all("div", {"class": "info-inner"}):
            label = div.find("div", {"class": "label"})
            if label and label.find("span").text == "aanvang":
                time = div.find("div", {"class": "values"}).find("span").text
        if event.when and time and len(time.split(":")) == 2:
            event.when = event.when.replace(hour=int(time.split(":")[0]), minute=int(time.split(":")[1]))
        return event


class TivoliProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = TivoliProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return super().processing_chain_with_additionals(client_session, database_sink)

    def fetch_source(self) -> Source:
        return TivoliSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="tivoli-utrecht",
            name="Tivoli Vredenburg",
            short_name="Tivoli NL-UTR",
            phone="030 - 2314544",
            city="Utrecht",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@tivolivredenburg.nl",
            source_url="https://www.tivolivredenburg.nl/agenda/",
            url="https://www.tivolivredenburg.nl",
        )


class TivoliSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand=",
    ):
        super().__init__(venue, scrape_url, TivoliParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=30)
