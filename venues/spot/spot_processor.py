from core.event_repository import EventRepository
from core.source import Source
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.spot.spot_config import SpotConfig
from venues.spot.spot_source import SpotSource


class SpotProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.config = SpotConfig()
        super().__init__(event_repository, venue_repository, self.config.venue())

    def fetch_source(self) -> Source:
        return SpotSource(self.config)

