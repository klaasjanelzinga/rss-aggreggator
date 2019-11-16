from aiohttp import ClientSession

from app.core.event.event_repository import EventRepository
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.paradiso_amsterdam.paradiso_source import ParadisoSource
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.processing_chain import Chain


class ParadisoProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = ParadisoProcessor.create_venue()
        venue_repository.register(self.venue)
        super().__init__(event_repository, self.venue)

    def fetch_source(self) -> Source:
        return ParadisoSource(self.venue)

    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return super().processing_chain_with_additionals(client_session, database_sink)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="paradiso-amsterdam",
            short_name="Paradiso NL-AMS",
            name="Paradiso Amsterdam",
            phone="",
            city="Amsterdam",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@paradiso.nl",
            url="https://www.paradiso.nl",
            source_url="https://www.paradiso.nl/",
        )
