from abc import ABC, abstractmethod
from typing import AsyncIterable, List

from aiohttp import ClientSession

from core_lib.core.models import Event, Venue
from core_lib.core.fetcher_util import fetch
from core_lib.core.parser import Parser, ParsingContext


class Source(ABC):
    def __init__(self, venue: Venue, scrape_url: str, parser: Parser):
        self.venue = venue
        self.scrape_url = scrape_url
        self.parser = parser

    async def fetch_page_in_one_call(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        data = await fetch(url=self.scrape_url, session=session)
        events = self.parser.parse(ParsingContext(venue=self.venue, content=data))
        yield events

    async def fetch_page_indexed(self, session: ClientSession, items_per_page: int) -> AsyncIterable[List[Event]]:
        page_index = 0
        done = False
        while not done:
            page_index += 1
            data = await fetch(url=self.scrape_url.format(page_index), session=session)
            new_events = self.parser.parse(ParsingContext(venue=self.venue, content=data))
            yield new_events
            done = len(new_events) < items_per_page

    async def fetch_event_detail(self, event: Event, client_session: ClientSession) -> str:
        return await fetch(url=event.url, session=client_session)

    @abstractmethod
    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        pass
