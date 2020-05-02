from aiohttp import ClientSession

from app.core.event.event_repository import EventRepository
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.processing_chain import Chain
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.tivoli_utrecht.tivoli_source import TivoliSource


class TivoliProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = TivoliProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return super().processing_chain_with_additionals(client_session, database_sink)

    def fetch_source(self) -> Source:
        return TivoliSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="tivoli-utrecht",
            name="Tivoli Vredenburg",
            short_name="Tivoli NL-UTR",
            phone="030 - 2314544",
            city="Utrecht",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@tivolivredenburg.nl",
            source_url="https://www.tivolivredenburg.nl/agenda/",
            url="https://www.tivolivredenburg.nl",
        )
