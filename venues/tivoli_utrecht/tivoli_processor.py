import logging

from core.app_config import AppConfig
from core.event_repository import EventRepository
from core.parsing_context import ParsingContext
from core.venue import Venue
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.tivoli_utrecht.tivoli_config import TivoliConfig
from venues.tivoli_utrecht.tivoli_fetcher import TivoliFetcher
from venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TivoliProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository):
        self.config = TivoliConfig()
        self.event_repository = event_repository
        self.venue = Venue(venue_id=self.config.venue_id,
                           name='Tivoli Vredenburg',
                           phone='030 - 2314544',
                           city='Utrecht',
                           country='NL',
                           timezone='Europe/Amsterdam',
                           email='info@tivolivredenburg.nl',
                           url=self.config.base_url)

    def sync_stores(self) -> None:
        fetcher = TivoliFetcher()
        parser = TivoliParser(self.config)
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
