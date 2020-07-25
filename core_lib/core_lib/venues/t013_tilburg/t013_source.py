from typing import AsyncIterable, List

from aiohttp import ClientSession

from core_lib.core.event.event import Event
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.venues.t013_tilburg.t013_parser import T013Parser


class T013Source(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.013.nl/programma"):
        super().__init__(venue, scrape_url, T013Parser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
