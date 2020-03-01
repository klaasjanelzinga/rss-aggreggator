from abc import ABC, abstractmethod
import asyncio
from datetime import datetime
import logging

from aiohttp import ClientSession

from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OC_TRACER, OpenCensusHelper
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.fetch_and_parse_details import FetchAndParseDetails
from app.core.processing_chain.only_changed_events import OnlyChangedEventsFilter
from app.core.processing_chain.only_valid_events import OnlyValidEvents
from app.core.processing_chain.processing_chain import Chain
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_repository import VenueRepository


class VenueProcessor(ABC):
    def __init__(
        self,
        event_repository: EventRepository,
        venue_repository: VenueRepository,
        venue: Venue,
        open_census_helper: OpenCensusHelper,
    ) -> None:
        self.event_repository = event_repository
        self.venue_repository = venue_repository
        self.venue = venue
        self.open_census_helper = open_census_helper
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
            with OC_TRACER.span(f"fetch_new_events") as span:
                span.add_annotation(self.venue.venue_id)
                fetched_events = await self.fetch_source().fetch_events(session)
                tasks = [
                    asyncio.create_task(chain.start_chain(fetched_event)) async for fetched_event in fetched_events
                ]
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
