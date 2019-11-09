from app.core.event.event import Event
from app.core.processing_chain.processing_chain import Link


class OnlyValidEvents(Link):
    async def chain(self, event: Event) -> None:
        if event.is_valid():
            await self.invoke_next_link(event)