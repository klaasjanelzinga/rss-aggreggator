import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime

from aiohttp import ClientSession

from core_lib.core.models import Venue
from core_lib.core.fetch_and_parse_details import FetchAndParseDetails
from core_lib.core.processing_chain import Chain, OnlyValidEvents, OnlyChangedEventsFilter, DatabaseSink
from core_lib.core.repositories import VenueRepository, EventRepository
from core_lib.core.source import Source


class VenueProcessor(ABC):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository, venue: Venue,) -> None:
        self.event_repository = event_repository
        self.venue_repository = venue_repository
        self.venue = venue
        self.logger = logging.getLogger(__name__)
        self.venue_repository.insert(self.venue)

    # pylint: disable= W0613, R0201
    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        existing_keys = self.event_repository.fetch_all_keys_as_string_for_venue(self.venue)
        only_changed_events_filter = OnlyChangedEventsFilter(existing_keys)
        return Chain([only_changed_events_filter, OnlyValidEvents(), database_sink])

    def processing_chain_with_additionals(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        existing_keys = self.event_repository.fetch_all_keys_as_string_for_venue(self.venue)
        only_changed_events_filter = OnlyChangedEventsFilter(existing_keys)

        return Chain(
            [
                only_changed_events_filter,
                OnlyValidEvents(),
                FetchAndParseDetails(client_session=client_session, source=self.fetch_source()),
                database_sink,
            ]
        )

    async def fetch_new_events(self, session: ClientSession) -> int:
        database_sink = DatabaseSink(self.event_repository)
        chain = self.create_processing_chain(session, database_sink)
        try:
            fetched_events = await self.fetch_source().fetch_events(session)
            tasks = [asyncio.create_task(chain.start_chain(fetched_event)) async for fetched_event in fetched_events]
            await asyncio.gather(*tasks)

            database_sink.flush()
            # self.open_census_helper.count_venue_total(self.venue, database_sink.total_sunk)
            logging.getLogger(__name__).info("Upserted %d events for %s", database_sink.total_sunk, self.venue.venue_id)
            self.venue.last_fetched_date = datetime.now()
            self.venue_repository.upsert(self.venue)
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
