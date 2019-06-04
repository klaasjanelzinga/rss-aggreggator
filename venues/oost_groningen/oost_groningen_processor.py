import logging

from core.event_repository import EventRepository
from core.parsing_context import ParsingContext
from core.venue import Venue
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.oost_groningen.oost_groningen_config import OostGroningenConfig
from venues.oost_groningen.oost_groningen_fetcher import OostGroningenFetcher
from venues.oost_groningen.oost_groningen_parser import OostGroningenParser


class OostGroningenProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = OostGroningenConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def sync_stores(self) -> None:
        fetcher = OostGroningenFetcher()
        parser = OostGroningenParser(self.config)
        data = fetcher.fetch()
        events = parser.parse(ParsingContext(venue=self.venue, content=data))
        logging.info(f'fetched a total of {len(events)} items from {self.venue}')
        self.event_repository.upsert(events)
