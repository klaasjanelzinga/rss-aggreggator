from typing import List

from app.core.event.event import Event
from app.core.event.event_repository import EventRepository
from app.core.processing_chain.processing_chain import Link


class DatabaseSink(Link):
    def __init__(self, event_repository: EventRepository) -> None:
        super().__init__()
        self.total_sunk = 0
        self.accumulator: List[Event] = []
        self.event_repository = event_repository

    async def chain(self, event: Event) -> None:
        self.accumulator.append(event)
        self.total_sunk += 1
        await self.invoke_next_link(event)

    def flush(self) -> None:
        sliced_events = DatabaseSink.slice_it(400, self.accumulator)
        for slice_of_events in sliced_events:
            self.event_repository.upsert_no_slicing(slice_of_events)

    @staticmethod
    def slice_it(batches: int, items: List[Event]) -> List[List[Event]]:
        result = []
        pivot = batches
        index = 0
        done = False
        while not done:
            actual = min(pivot + index, len(items))
            first = items[index : actual + index]
            done = actual == len(items)
            result.append(first)
            index += pivot
        return result
