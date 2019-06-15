from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue_processor import VenueProcessor
from app.core.venue_repository import VenueRepository
from app.venues.melkweg_amsterdam.melkweg_config import MelkwegConfig
from app.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


class MelkwegProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = MelkwegConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return MelkwegSource(self.config)

