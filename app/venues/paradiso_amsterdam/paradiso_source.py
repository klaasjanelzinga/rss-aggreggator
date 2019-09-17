from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.paradiso_amsterdam.paradiso_parser import ParadisoParser


class ParadisoSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://api.paradiso.nl/api/events'
                                   '?lang=en&start_time=now&sort=date&order=asc&limit=30&page={}&with=locations'):
        self.venue = venue
        self.scrape_url = scrape_url

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return Source.fetch_page_indexed(session=session,
                                         parser=ParadisoParser(),
                                         venue=self.venue,
                                         scrape_url_format=self.scrape_url,
                                         items_per_page=30)
