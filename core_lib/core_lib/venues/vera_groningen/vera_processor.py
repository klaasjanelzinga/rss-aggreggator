from core_lib.core.event.event_repository import EventRepository
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.core.venue.venue_processor import VenueProcessor
from core_lib.core.venue.venue_repository import VenueRepository
from core_lib.venues.vera_groningen.vera_source import VeraSource


class VeraProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = VeraProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return VeraSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="vera-groningen",
            name="VERA-Groningen",
            short_name="Vera NL-GRN",
            phone="+31 (0)50 313 46 81",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@vera-groningen.nl",
            source_url="https://www.vera-groningen.nl/programma/",
            url="https://www.vera-groningen.nl",
        )
