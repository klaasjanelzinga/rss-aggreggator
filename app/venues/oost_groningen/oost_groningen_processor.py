from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.oost_groningen.oost_groningen_source import OostGroningenSource


class OostGroningenProcessor(VenueProcessor):
    def __init__(
        self, event_repository: EventRepository, venue_repository: VenueRepository, open_census_helper: OpenCensusHelper
    ):
        self.venue = OostGroningenProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue, open_census_helper)

    def fetch_source(self) -> Source:
        return OostGroningenSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="oost-groningen",
            short_name="Oost NL-GRN",
            name="Oost Groningen",
            phone="",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@komoost.nl",
            url="https://www.komoost.nl",
            source_url="https://www.komoost.nl",
        )
