from typing import List, AsyncIterable

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.vera_groningen.vera_parser import VeraParser


class VeraSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.vera-groningen.nl/wp/wp-admin/admin-ajax.php?"
        "action=renderProgramme&category=all&page={}&perpage=20&lang=nl",
    ):
        super().__init__(venue, scrape_url, VeraParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=20)
