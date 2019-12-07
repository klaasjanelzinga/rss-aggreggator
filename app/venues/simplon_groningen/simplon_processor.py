from opencensus.stats.measure import MeasureInt

from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import create_count_measurement_for_venue
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.simplon_groningen.simplon_source import SimplonSource


class SimplonProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SimplonProcessor.create_venue()
        venue_repository.register(self.venue)
        self.oc_number_of_events_measure = create_count_measurement_for_venue(self.venue)
        super().__init__(event_repository, self.venue)

    def fetch_source(self) -> Source:
        return SimplonSource(self.venue)

    def number_of_events_measure(self) -> MeasureInt:
        return self.oc_number_of_events_measure

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
