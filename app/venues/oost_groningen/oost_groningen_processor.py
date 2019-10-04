from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.oost_groningen.oost_groningen_source import OostGroningenSource


class OostGroningenProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = OostGroningenProcessor.create_venue()
        venue_repository.register(self.venue)
        super().__init__(event_repository, self.venue)

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
            timezone_short="+02:00",
            email="info@komoost.nl",
            url="https://www.komoost.nl",
            source_url="https://www.komoost.nl",
        )
