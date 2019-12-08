import logging
from abc import ABC, abstractmethod
from datetime import datetime

from aiohttp import ClientSession
from opencensus.stats.measure import MeasureInt
from opencensus.stats.stats import stats
from opencensus.tags import tag_key, tag_map, tag_value

from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OC_TRACER
from app.core.processing_chain.database_sink import DatabaseSink
from app.core.processing_chain.fetch_and_parse_details import FetchAndParseDetails
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

    def processing_chain_with_additionals(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return Chain(
            [
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
                async for fetched_events in await self.fetch_source().fetch_events(session=session):
                    await chain.start_chain(fetched_events)

            database_sink.flush()
            mmap = stats.stats_recorder.new_measurement_map()
            mmap.measure_int_put(self.number_of_events_measure(), database_sink.total_sunk)
            tmap = tag_map.TagMap()
            tmap.insert(tag_key.TagKey("venue_id"), tag_value.TagValue(self.venue.venue_id))
            mmap.record(tmap)
            logging.getLogger(__name__).info("Upserted %d events for %s", database_sink.total_sunk, self.venue.venue_id)
            self.venue.last_fetched_date = datetime.now()
        # pylint: disable=W0703
        except Exception as exception:
            logging.getLogger(__name__).exception("Unable to sync %s %s", self.venue.venue_id, exception)
        return database_sink.total_sunk

    @abstractmethod
    def fetch_source(self) -> Source:
        pass

    @abstractmethod
    def number_of_events_measure(self) -> MeasureInt:
        pass

    @staticmethod
    @abstractmethod
    def create_venue() -> Venue:
        pass
