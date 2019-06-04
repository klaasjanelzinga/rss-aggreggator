from core.event_repository import EventRepository
from core.source import Source
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.paradiso_amsterdam.paradiso_config import ParadisoConfig
from venues.paradiso_amsterdam.paradiso_source import ParadisoSource


class ParadisoProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = ParadisoConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return ParadisoSource(self.config)

