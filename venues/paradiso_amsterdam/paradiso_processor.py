import logging

from core.event_repository import EventRepository
from core.parsing_context import ParsingContext
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.paradiso_amsterdam.paradiso_config import ParadisoConfig
from venues.paradiso_amsterdam.paradiso_fetcher import ParadisoFetcher
from venues.paradiso_amsterdam.paradiso_parser import ParadisoParser


class ParadisoProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = ParadisoConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

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
