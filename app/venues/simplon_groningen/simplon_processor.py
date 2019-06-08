from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue_processor import VenueProcessor
from app.core.venue_repository import VenueRepository
from app.venues.simplon_groningen.simplon_config import SimplonConfig
from app.venues.simplon_groningen.simplon_source import SimplonSource


class SimplonProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = SimplonConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return SimplonSource(self.config)

