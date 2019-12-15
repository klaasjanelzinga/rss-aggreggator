from aiohttp import ClientSession

from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.fetch_and_parse_details import FetchAndParseDetails
from app.core.processing_chain.only_valid_events import OnlyValidEvents
from app.core.processing_chain.processing_chain import Chain
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.neushoorn_leeuwarden.neushoorn_source import NeushoornSource


class NeushoornProcessor(VenueProcessor):
    def __init__(
        self, event_repository: EventRepository, venue_repository: VenueRepository, open_census_helper: OpenCensusHelper
    ):
        self.venue = NeushoornProcessor.create_venue()
        venue_repository.register(self.venue)
        super().__init__(event_repository, self.venue, open_census_helper)

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
            short_name="Neus LEE",
            name="Neushoorn Leeuwarden",
            phone="",
            city="Leeuwarden",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@neushoorn.nl",
            url="https://www.neushoorn.nl",
            source_url="https://www.neushoorn.nl",
        )
