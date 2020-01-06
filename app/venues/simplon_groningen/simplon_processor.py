from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.simplon_groningen.simplon_source import SimplonSource


class SimplonProcessor(VenueProcessor):
    def __init__(
        self, event_repository: EventRepository, venue_repository: VenueRepository, open_census_helper: OpenCensusHelper
    ):
        self.venue = SimplonProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue, open_census_helper)

    def fetch_source(self) -> Source:
        return SimplonSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="simplon-groningen",
            name="Simplon Groningen",
            short_name="Simplon NL-GRN",
            phone="0503184150",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@simplon.nl",
            source_url="https://www.simplon.nl/agenda",
            url="https://www.simplon.nl",
        )
