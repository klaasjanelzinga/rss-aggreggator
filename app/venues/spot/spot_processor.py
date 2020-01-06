from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.spot.spot_source import SpotSource


class SpotProcessor(VenueProcessor):
    def __init__(
        self, event_repository: EventRepository, venue_repository: VenueRepository, open_census_helper: OpenCensusHelper
    ):
        self.venue = SpotProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue, open_census_helper)

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
