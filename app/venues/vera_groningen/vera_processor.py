from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue_processor import VenueProcessor
from app.core.venue_repository import VenueRepository
from app.venues.vera_groningen.vera_config import VeraConfig
from app.venues.vera_groningen.vera_source import VeraSource


class VeraProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = VeraConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return VeraSource(self.config)

