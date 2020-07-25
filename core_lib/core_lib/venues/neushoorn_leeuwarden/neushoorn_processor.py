from aiohttp import ClientSession

from core_lib.core.event.event_repository import EventRepository
from core_lib.core.processing_chain.database_sink import DatabaseSink
from core_lib.core.processing_chain.fetch_and_parse_details import FetchAndParseDetails
from core_lib.core.processing_chain.only_valid_events import OnlyValidEvents
from core_lib.core.processing_chain.processing_chain import Chain
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.core.venue.venue_processor import VenueProcessor
from core_lib.core.venue.venue_repository import VenueRepository
from core_lib.venues.neushoorn_leeuwarden.neushoorn_source import NeushoornSource


class NeushoornProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = NeushoornProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return NeushoornSource(self.venue)

    # pylint: disable= W0613, R0201
    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return Chain(
            [
                FetchAndParseDetails(client_session=client_session, source=self.fetch_source()),
                OnlyValidEvents(),
                database_sink,
            ]
        )

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="neushoorn-leeuwarden",
            short_name="Neus NL-LEE",
            name="Neushoorn Leeuwarden",
            phone="",
            city="Leeuwarden",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@neushoorn.nl",
            url="https://www.neushoorn.nl",
            source_url="https://www.neushoorn.nl",
        )
