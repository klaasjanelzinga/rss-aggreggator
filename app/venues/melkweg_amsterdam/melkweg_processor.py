from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


class MelkwegProcessor(VenueProcessor):
    def __init__(
        self, event_repository: EventRepository, venue_repository: VenueRepository, open_census_helper: OpenCensusHelper
    ):
        self.venue = MelkwegProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue, open_census_helper)

    def fetch_source(self) -> Source:
        return MelkwegSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="melkweg-amsterdam",
            short_name="Melkweg NL-AMS",
            name="Melkweg Amsterdam",
            phone="",
            city="Amsterdam",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@melkweg.nl",
            source_url="https://www.melkweg.nl/agenda",
            url="https://www.melkweg.nl",
        )
