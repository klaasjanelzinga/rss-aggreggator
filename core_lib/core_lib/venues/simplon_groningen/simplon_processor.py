from core_lib.core.event.event_repository import EventRepository
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.core.venue.venue_processor import VenueProcessor
from core_lib.core.venue.venue_repository import VenueRepository
from core_lib.venues.simplon_groningen.simplon_source import SimplonSource


class SimplonProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SimplonProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

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
