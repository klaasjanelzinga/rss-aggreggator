from typing import AsyncIterable, List

from aiohttp import ClientSession

from core_lib.core.event.event import Event
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.venues.vera_groningen.vera_parser import VeraParser


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
