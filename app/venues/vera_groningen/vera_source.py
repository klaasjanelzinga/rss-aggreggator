from typing import List, AsyncIterable, Coroutine, Any

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.vera_groningen.vera_parser import VeraParser


class VeraSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.vera-groningen.nl/wp/wp-admin/admin-ajax.php?'
                                   'action=renderProgramme&category=all&page={}&perpage=20&lang=nl'):
        self.venue = venue
        self.scrape_url = scrape_url

    async def fetch_events(self, session: ClientSession) -> Coroutine[Any, Any, AsyncIterable[List[Event]]]:
        return Source.fetch_page_indexed(parser=VeraParser(),
                                         venue=self.venue,
                                         session=session,
                                         scrape_url_format=self.scrape_url,
                                         items_per_page=20)
