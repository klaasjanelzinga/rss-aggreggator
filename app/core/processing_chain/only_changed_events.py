from typing import List

from app.core.event.event import Event
from app.core.processing_chain.processing_chain import Link


class OnlyChangedEventsFilter(Link):
    def __init__(self, existing_keys: List[str]):
        super().__init__()
        self.existing_keys = existing_keys

    async def chain(self, event: Event) -> None:
        if event.event_id not in self.existing_keys:
            await self.invoke_next_link(event)
