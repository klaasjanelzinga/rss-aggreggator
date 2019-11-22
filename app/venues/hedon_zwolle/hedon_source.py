from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.hedon_zwolle.hedon_parser import HedonParser


class HedonSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.hedon-zwolle.nl/#programma"):
        super().__init__(venue, scrape_url, HedonParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
