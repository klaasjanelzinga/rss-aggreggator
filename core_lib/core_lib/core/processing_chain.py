from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from core_lib.core.models import Event
from core_lib.core.repositories import EventRepository


class Link(ABC):
    def __init__(self) -> None:
        self.next_link: Optional[Link] = None

    @abstractmethod
    async def chain(self, event: Event) -> None:
        pass

    async def invoke_next_link(self, event: Event) -> None:
        if self.next_link:
            await self.next_link.chain(event)


class Chain:
    def __init__(self, chain: List[Link]) -> None:
        self.chain = chain
        for i, link in enumerate(self.chain[:-1]):
            link.next_link = self.chain[i + 1]

    async def start_chain(self, events: List[Event]) -> None:
        for event in events:
            await self.chain[0].chain(event)


class OnlyValidEvents(Link):
    async def chain(self, event: Event) -> None:
        if event.is_valid():
            await self.invoke_next_link(event)


class OnlyChangedEventsFilter(Link):
    def __init__(self, existing_keys: List[str]):
        super().__init__()
        self.existing_keys = existing_keys

    async def chain(self, event: Event) -> None:
        if event.event_id not in self.existing_keys:
            await self.invoke_next_link(event)


class OnlyEventsWithWhen(Link):
    async def chain(self, event: Event) -> None:
        if event.when is not None:
            await self.invoke_next_link(event)


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
            first = items[index : (actual + index)]
            done = actual == len(items)
            result.append(first)
            index += pivot
        return result
