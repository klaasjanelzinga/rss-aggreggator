from abc import ABC, abstractmethod
from typing import List, Optional

from core_lib.core.event.event import Event


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
