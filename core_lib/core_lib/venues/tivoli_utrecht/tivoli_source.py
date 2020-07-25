from typing import AsyncIterable, List

from aiohttp import ClientSession

from core_lib.core.event.event import Event
from core_lib.core.source import Source
from core_lib.core.venue.venue import Venue
from core_lib.venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TivoliSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand=",
    ):
        super().__init__(venue, scrape_url, TivoliParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=30)
