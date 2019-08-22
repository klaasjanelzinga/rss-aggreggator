from typing import AsyncIterable, List, Coroutine, Any

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TivoliSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str =
                 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand='):
        self.venue = venue
        self.scrape_url = scrape_url

    async def fetch_events(self, session: ClientSession) -> Coroutine[Any, Any, AsyncIterable[List[Event]]]:
        return Source.fetch_page_indexed(session=session,
                                         parser=TivoliParser(),
                                         venue=self.venue,
                                         scrape_url_format=self.scrape_url,
                                         items_per_page=30)
