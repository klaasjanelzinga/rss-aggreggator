from typing import AsyncIterable, List

from aiohttp import ClientSession

from core_lib.core.event.event import Event
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.venues.neushoorn_leeuwarden.neushoorn_parser import NeushoornParser


class NeushoornSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://neushoorn.nl/upcoming_events"):
        super().__init__(venue, scrape_url, NeushoornParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
