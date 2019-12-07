from opencensus.stats.measure import MeasureInt

from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import create_count_measurement_for_venue
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.spot.spot_source import SpotSource


class SpotProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SpotProcessor.create_venue()
        venue_repository.register(self.venue)
        self.oc_number_of_events_measure = create_count_measurement_for_venue(self.venue)
        super().__init__(event_repository, self.venue)

    def fetch_source(self) -> Source:
        return SpotSource(self.venue)

    def number_of_events_measure(self) -> MeasureInt:
        return self.oc_number_of_events_measure

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="spot-groningen",
            name="SPOT",
            short_name="Spot NL-GRN",
            phone="+31 (0)50-3680111",
            city="Groningen",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@spotgroningen.nl",
            url="https://www.spotgroningen.nl",
            source_url="https://www.spotgroningen.nl/programma",
        )
