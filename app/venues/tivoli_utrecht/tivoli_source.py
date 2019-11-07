from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TivoliSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand=",
    ):
        super().__init__(venue, scrape_url, TivoliParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_indexed(session=session, items_per_page=30)
