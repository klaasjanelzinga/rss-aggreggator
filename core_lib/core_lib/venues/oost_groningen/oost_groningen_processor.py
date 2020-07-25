from core_lib.core.event.event_repository import EventRepository
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.core.venue.venue_processor import VenueProcessor
from core_lib.core.venue.venue_repository import VenueRepository
from core_lib.venues.oost_groningen.oost_groningen_source import OostGroningenSource


class OostGroningenProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = OostGroningenProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

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
