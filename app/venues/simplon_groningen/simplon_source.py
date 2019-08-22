from typing import AsyncIterable, List, Coroutine, Any

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.simplon_groningen.simplon_parser import SimplonParser


class SimplonSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.simplon.nl'):
        self.venue = venue
        self.scrape_url = scrape_url

    async def fetch_events(self, session: ClientSession) -> Coroutine[Any, Any, AsyncIterable[List[Event]]]:
        return Source.fetch_page_in_one_call(session=session,
                                             parser=SimplonParser(),
                                             venue=self.venue,
                                             scrape_url=self.scrape_url)
