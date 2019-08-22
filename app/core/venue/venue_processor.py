import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from aiohttp import ClientSession

from app.core.event import Event
from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue.venue import Venue


class VenueProcessor(ABC):

    def __init__(self, event_repository: EventRepository, venue: Venue):
        self.event_repository = event_repository
        self.venue = venue
        self.logger = logging.getLogger(__name__)

    async def async_store(self, session: ClientSession) -> int:
        try:
            total = 0
            accumulator = []
            async for fetched_events in await self.fetch_source().fetch_events(session=session):
                events = [e for e in fetched_events if e.is_valid()]
                accumulator.extend(events)
                total += len(events)
                events = VenueProcessor.slice_it(400, events)
                for slice_of_events in events:
                    self.event_repository.upsert_no_slicing(slice_of_events)

            logging.getLogger(__name__).info('Upserted %d events for %s', total, self.venue.venue_id)
            self.venue.last_fetched_date = datetime.now()
            return total
        # pylint: disable=W0703
        except Exception as exception:
            logging.getLogger(__name__).exception('Unable to sync %s %s', self.venue.venue_id, exception)

    @staticmethod
    def slice_it(batches: int, items: List[Event]) -> List[List[Event]]:
        result = []
        pivot = batches
        index = 0
        done = False
        while not done:
            actual = min(pivot+index, len(items))
            first = items[index:actual+index]
            done = actual == len(items)
            result.append(first)
            index += pivot
        return result

    @abstractmethod
    def fetch_source(self) -> Source:
        pass

    @staticmethod
    @abstractmethod
    def create_venue() -> Venue:
        pass
