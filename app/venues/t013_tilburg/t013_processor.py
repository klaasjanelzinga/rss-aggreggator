from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.t013_tilburg.t013_source import T013Source


class T013Processor(VenueProcessor):
    def __init__(
        self, event_repository: EventRepository, venue_repository: VenueRepository, open_census_helper: OpenCensusHelper
    ):
        self.venue = T013Processor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue, open_census_helper)

    def fetch_source(self) -> Source:
        return T013Source(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="013-tilburg",
            name="013 Tilburg",
            short_name="013 NL-TIL",
            phone="+31 (0)13-4609500",
            city="Tilburg",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@013.nl",
            url="https://www.013.nl",
            source_url="https://www.013.nl/programma",
        )
