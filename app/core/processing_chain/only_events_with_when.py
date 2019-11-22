from datetime import datetime

from app.core.event.event import Event
from app.core.processing_chain.processing_chain import Link


class OnlyEventsWithWhen(Link):
    async def chain(self, event: Event) -> None:
        if event.when is not None and event.when != datetime.min:
            await self.invoke_next_link(event)
