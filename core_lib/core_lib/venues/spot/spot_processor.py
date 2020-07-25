from core_lib.core.event.event_repository import EventRepository
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.core.venue.venue_processor import VenueProcessor
from core_lib.core.venue.venue_repository import VenueRepository
from core_lib.venues.spot.spot_source import SpotSource


class SpotProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SpotProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return SpotSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="spot-groningen",
            name="SPOT",
            short_name="Spot NL-GRN",
            phone="+31 (0)50-3680111",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@spotgroningen.nl",
            url="https://www.spotgroningen.nl",
            source_url="https://www.spotgroningen.nl/programma",
        )
