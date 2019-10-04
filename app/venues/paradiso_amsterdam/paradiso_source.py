from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.paradiso_amsterdam.paradiso_parser import ParadisoParser


class ParadisoSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://api.paradiso.nl/api/events"
        "?lang=en&start_time=now&sort=date&order=asc&limit=30&page={}&with=locations",
    ):
        super().__init__(venue, scrape_url, ParadisoParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=30)
