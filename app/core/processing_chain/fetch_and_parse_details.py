from aiohttp import ClientSession

from app.core.event.event import Event
from app.core.processing_chain.processing_chain import Link
from app.core.source import Source


class FetchAndParseDetails(Link):
    def __init__(self, source: Source, client_session: ClientSession):
        super().__init__()
        self.source = source
        self.client_session = client_session

    async def chain(self, event: Event) -> None:
        additional_data = await self.source.fetch_event_detail(event=event, client_session=self.client_session)
        event = self.source.parser.update_event_with_details(event=event, additional_details=additional_data)
        await self.invoke_next_link(event)
