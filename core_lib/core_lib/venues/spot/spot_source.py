from typing import AsyncIterable, List

from aiohttp import ClientSession

from core_lib.core.event.event import Event
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.venues.spot.spot_parser import SpotParser


class SpotSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.spotgroningen.nl/programma"):
        super().__init__(venue, scrape_url, SpotParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
