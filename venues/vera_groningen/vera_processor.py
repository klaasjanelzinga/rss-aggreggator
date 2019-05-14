import logging

from core.event_repository import EventRepository
from core.parsing_context import ParsingContext
from core.venue import Venue
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.vera_groningen.vera_config import VeraConfig
from venues.vera_groningen.vera_fetcher import VeraFetcher
from venues.vera_groningen.vera_parser import VeraParser


class VeraProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository):
        self.config = VeraConfig()
        self.event_repository = event_repository
        self.venue = Venue(venue_id=self.config.venue_id,
                           name='VERA-Groningen',
                           phone='+31 (0)50 313 46 81',
                           city='Groningen',
                           country='NL',
                           timezone=self.config.timezone,
                           email='info@vera-groningen.nl',
                           url=self.config.base_url)

    def sync_stores(self) -> None:
        vera_fetcher = VeraFetcher()
        vera_parser = VeraParser(self.config)
        items_per_page = 20

        done = False
        events = []
        while not done:
            page_index =+ 1
            data = vera_fetcher.fetch(page_index, items_per_page)
            new_events = vera_parser.parse(ParsingContext(venue=self.venue, content=data))
            done = len(new_events) < items_per_page
            events.extend(new_events)
        logging.info(f'fetched a total of {len(events)} items from {self.venue}')
        self.event_repository.upsert(events)

    def register_venue_at(self, venue_repository: VenueRepository):
        venue_repository.register(self.config.venue_id, self.venue, self)
