from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue_processor import VenueProcessor
from app.core.venue_repository import VenueRepository
from app.venues.tivoli_utrecht.tivoli_config import TivoliConfig
from app.venues.tivoli_utrecht.tivoli_source import TivoliSource


class TivoliProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = TivoliConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return TivoliSource(self.config)

