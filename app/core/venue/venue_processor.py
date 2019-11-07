import logging
from abc import ABC, abstractmethod
from datetime import datetime

from aiohttp import ClientSession

from app.core.event.event_repository import EventRepository
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.only_valid_events import OnlyValidEvents
from app.core.processing_chain.processing_chain import Chain
from app.core.source import Source
from app.core.venue.venue import Venue


class VenueProcessor(ABC):
    def __init__(self, event_repository: EventRepository, venue: Venue) -> None:
        self.event_repository = event_repository
        self.venue = venue
        self.logger = logging.getLogger(__name__)

    # pylint: disable= W0613, R0201
    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return Chain([OnlyValidEvents(), database_sink])

    async def fetch_new_events(self, session: ClientSession) -> int:
        database_sink = DatabaseSink(self.event_repository)
        chain = self.create_processing_chain(session, database_sink)
        try:
            async for fetched_events in await self.fetch_source().fetch_events(session=session):
                await chain.start_chain(fetched_events)

            database_sink.flush()
            logging.getLogger(__name__).info("Upserted %d events for %s", database_sink.total_sunk, self.venue.venue_id)
            self.venue.last_fetched_date = datetime.now()
        # pylint: disable=W0703
        except Exception as exception:
            logging.getLogger(__name__).exception("Unable to sync %s %s", self.venue.venue_id, exception)
        return database_sink.total_sunk

    @abstractmethod
    def fetch_source(self) -> Source:
        pass

    @staticmethod
    @abstractmethod
    def create_venue() -> Venue:
        pass
