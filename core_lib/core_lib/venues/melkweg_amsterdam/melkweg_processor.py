from core_lib.core.event.event_repository import EventRepository
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.core.venue.venue_processor import VenueProcessor
from core_lib.core.venue.venue_repository import VenueRepository
from core_lib.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


class MelkwegProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = MelkwegProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

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
