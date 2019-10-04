from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.simplon_groningen.simplon_parser import SimplonParser


class SimplonSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.simplon.nl"):
        super().__init__(venue, scrape_url, SimplonParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
