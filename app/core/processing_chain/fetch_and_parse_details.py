import asyncio
import concurrent
import logging
from json import JSONDecodeError

from aiohttp import ClientSession
from aiohttp.client import ServerDisconnectedError

from app.core.event.event import Event
from app.core.processing_chain.processing_chain import Link
from app.core.source import Source


class FetchAndParseDetails(Link):
    def __init__(self, source: Source, client_session: ClientSession):
        super().__init__()
        self.source = source
        self.client_session = client_session
        self.logger = logging.getLogger(__name__)

    async def chain(self, event: Event) -> None:
        try:
            additional_data = await self.source.fetch_event_detail(event=event, client_session=self.client_session)
            event = self.source.parser.update_event_with_details(event=event, additional_details=additional_data)
        except JSONDecodeError:
            self.logger.info("Exception parsing response for details, event %s for %s", event, event.venue)
        except (concurrent.futures.TimeoutError, asyncio.TimeoutError):
            self.logger.info("Timeout fetching response for details, event %s for %s", event, event.venue)
        except ServerDisconnectedError:
            self.logger.info("Server disconnected error response for details, event %s for %s", event, event.venue)
        await self.invoke_next_link(event)
