from core.event_repository import EventRepository
from core.source import Source
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.oost_groningen.oost_groningen_config import OostGroningenConfig
from venues.oost_groningen.oost_groningen_source import OostGroningenSource


class OostGroningenProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = OostGroningenConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return OostGroningenSource(self.config)

