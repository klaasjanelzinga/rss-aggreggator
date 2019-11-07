from app.core.event.event import Event
from app.core.processing_chain.processing_chain import Link


class OnlyChangedEvents(Link):
    async def chain(self, event: Event) -> None:
        # fetch from store
        # check heads
        await self.invoke_next_link(event)
