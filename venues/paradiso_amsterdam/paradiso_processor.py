import logging

from core.app_config import AppConfig
from core.event_repository import EventRepository
from core.parsing_context import ParsingContext
from core.venue import Venue
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.paradiso_amsterdam.paradiso_config import ParadisoConfig
from venues.paradiso_amsterdam.paradiso_fetcher import ParadisoFetcher
from venues.paradiso_amsterdam.paradiso_parser import ParadisoParser
from venues.tivoli_utrecht.tivoli_config import TivoliConfig
from venues.tivoli_utrecht.tivoli_fetcher import TivoliFetcher
from venues.tivoli_utrecht.tivoli_parser import TivoliParser


class ParadisoProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository):
        self.config = ParadisoConfig()
        self.event_repository = event_repository
        self.venue = Venue(venue_id=self.config.venue_id,
                           name='Paradiso Amsterdam',
                           phone='',
                           city='Amsterdam',
                           country='NL',
                           timezone='Europe/Amsterdam',
                           email='info@paradiso.nl',
                           url=self.config.base_url)

    def sync_stores(self) -> None:
        fetcher = ParadisoFetcher()
        parser = ParadisoParser(self.config)

        page_index = 0
        done = False
        events = []
        while not done:
            page_index += 1
            data = fetcher.fetch(page_index)
            new_events = parser.parse(ParsingContext(venue=self.venue, content=data))
            done = len(new_events) < 30
            events.extend(new_events)
        logging.info(f'fetched a total of {len(events)} items from {self.venue}')
        self.event_repository.upsert(events)

    def register_venue_at(self, venue_repository: VenueRepository):
        venue_repository.register(self.config.venue_id, self.venue, self)
