from abc import ABC, abstractmethod
from typing import List, AsyncIterable

from aiohttp import ClientSession

from app.core.event import Event
from app.core.fetcher_util import fetch
from app.core.parser import Parser
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class Source(ABC):

    @staticmethod
    async def fetch_page_in_one_call(session: ClientSession,
                                     parser: Parser,
                                     venue: Venue,
                                     scrape_url: str) -> AsyncIterable[List[Event]]:
        data = await fetch(url=scrape_url, session=session)
        events = parser.parse(ParsingContext(venue=venue, content=data))
        yield events

    @staticmethod
    async def fetch_page_indexed(session: ClientSession,
                                 parser: Parser,
                                 venue: Venue,
                                 scrape_url_format: str,
                                 items_per_page: int) -> AsyncIterable[List[Event]]:
        page_index = 0
        done = False
        while not done:
            page_index += 1
            data = await fetch(url=scrape_url_format.format(page_index), session=session)
            new_events = parser.parse(ParsingContext(venue=venue, content=data))
            yield new_events
            done = len(new_events) < items_per_page

    @abstractmethod
    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        pass
