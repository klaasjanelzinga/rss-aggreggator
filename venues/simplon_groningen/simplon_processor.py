import logging

from core.event_repository import EventRepository
from core.venue import Venue
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.simplon_groningen.simplon_config import SimplonConfig
from venues.simplon_groningen.simplon_fetcher import SimplonFetcher
from venues.simplon_groningen.simplon_parser import SimplonParser


class SimplonProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository):
        self.config = SimplonConfig()
        self.event_repository = event_repository

    def create_venue(self) -> Venue:
        return Venue(venue_id=self.config.venue_id,
                     name='Simplon Groningen',
                     phone='0503184150',
                     city='Groningen',
                     country='NL',
                     timezone=self.config.timezone,
                     email='info@simplon.nl',
                     url=self.config.base_url)

    def sync_stores(self) -> None:
        fetcher = SimplonFetcher()
        parser = SimplonParser(self.config)
        data = fetcher.fetch()
        events = parser.parse(data)
        logging.info(f'fetched a total of {len(events)} items')
        self.event_repository.upsert(events)

    def register_venue_at(self, venue_repository: VenueRepository):
        venue_repository.register(self.config.venue_id, self.create_venue(), self)
