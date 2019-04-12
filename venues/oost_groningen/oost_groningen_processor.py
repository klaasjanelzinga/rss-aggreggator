import logging

from core.event_repository import EventRepository
from core.venue import Venue
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.oost_groningen.oost_groningen_config import OostGroningenConfig
from venues.oost_groningen.oost_groningen_fetcher import OostGroningenFetcher
from venues.oost_groningen.oost_groningen_parser import OostGroningenParser


class OostGroningenProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository):
        self.config = OostGroningenConfig()
        self.event_repository = event_repository
        self.venue = Venue(venue_id=self.config.venue_id,
                           name='Oost Groningen',
                           phone='',
                           city='Groningen',
                           country='NL',
                           timezone=self.config.timezone,
                           email='info@komoost.nl',
                           url=self.config.base_url)

    def sync_stores(self) -> None:
        fetcher = OostGroningenFetcher()
        parser = OostGroningenParser(self.config)
        data = fetcher.fetch()
        events = parser.parse(data)
        logging.info(f'fetched a total of {len(events)} items from {self.venue}')
        self.event_repository.upsert(events)

    def register_venue_at(self, venue_repository: VenueRepository):
        venue_repository.register(self.config.venue_id, self.venue, self)
