from core.event_repository import EventRepository
from core.source import Source
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.simplon_groningen.simplon_config import SimplonConfig
from venues.simplon_groningen.simplon_source import SimplonSource


class SimplonProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = SimplonConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return SimplonSource(self.config)

