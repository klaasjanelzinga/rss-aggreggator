from typing import AsyncIterable, List, Any, Coroutine

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.spot.spot_parser import SpotParser


class SpotSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.spotgroningen.nl/programma'):
        self.venue = venue
        self.scrape_url = scrape_url

    async def fetch_events(self, session: ClientSession) -> Coroutine[Any, Any, AsyncIterable[List[Event]]]:
        return Source.fetch_page_in_one_call(session=session,
                                             parser=SpotParser(),
                                             venue=self.venue,
                                             scrape_url=self.scrape_url)
