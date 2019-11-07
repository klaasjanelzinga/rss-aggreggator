from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.oost_groningen.oost_groningen_parser import OostGroningenParser


class OostGroningenSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.komoost.nl"):
        super().__init__(venue, scrape_url, OostGroningenParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
