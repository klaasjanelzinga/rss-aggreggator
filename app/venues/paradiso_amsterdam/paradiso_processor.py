from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue_processor import VenueProcessor
from app.core.venue_repository import VenueRepository
from app.venues.paradiso_amsterdam.paradiso_config import ParadisoConfig
from app.venues.paradiso_amsterdam.paradiso_source import ParadisoSource


class ParadisoProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = ParadisoConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return ParadisoSource(self.config)

