from typing import AsyncIterable, List

from aiohttp import ClientSession

from app.core.event.event import Event
from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.melkweg_amsterdam.melkweg_parser import MelkwegParser


class MelkwegSource(Source):
    def __init__(
        self,
        venue: Venue,
        scrape_url: str = "https://www.melkweg.nl/nl/agenda/as_json/1/grouped/0/page_size/-1?cb=2603211",
    ):
        super().__init__(venue, scrape_url, MelkwegParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
