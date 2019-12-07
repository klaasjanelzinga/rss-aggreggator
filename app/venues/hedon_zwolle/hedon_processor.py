from aiohttp import ClientSession
from opencensus.stats.measure import MeasureInt

from app.core.app_config import AppConfig
from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import create_count_measurement_for_venue
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.only_events_with_when import OnlyEventsWithWhen
from app.core.processing_chain.processing_chain import Chain
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.hedon_zwolle.hedon_source import HedonSource


class HedonProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = HedonProcessor.create_venue()
        venue_repository.register(self.venue)
        self.oc_number_of_events_measure = create_count_measurement_for_venue(self.venue)
        super().__init__(event_repository, self.venue)

    def fetch_source(self) -> Source:
        return HedonSource(self.venue)

    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        if AppConfig.is_running_in_gae():
            return super().create_processing_chain(client_session, database_sink)
        return Chain([OnlyEventsWithWhen(), database_sink])

    def number_of_events_measure(self) -> MeasureInt:
        return self.oc_number_of_events_measure

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="hedon-zwolle",
            name="Hedon",
            short_name="Hedon NL-ZWO",
            phone="+31 038-452 72 29",
            city="Zwolle",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@hedon-zwolle.nl",
            url="https://www.hedon-zwolle.nl",
            source_url="https://www.hedon-zwolle.nl/#programma",
        )
