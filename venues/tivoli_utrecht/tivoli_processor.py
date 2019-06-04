from core.event_repository import EventRepository
from core.source import Source
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.tivoli_utrecht.tivoli_config import TivoliConfig
from venues.tivoli_utrecht.tivoli_source import TivoliSource


class TivoliProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = TivoliConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return TivoliSource(self.config)

