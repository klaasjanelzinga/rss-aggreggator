import logging
from typing import List

from core.event import Event
from core.event_repository import EventRepository
from core.venue import Venue
from spot.config import SpotConfig
from spot.fetcher import SpotFetcher
from spot.parser import SpotParser


class SpotProcessor:

    def __init__(self, event_repository: EventRepository):
        self.config = SpotConfig()
        self.event_repository = event_repository

    def create_venue(self, items: List[Event]) -> Venue:
        return Venue(venue_id=self.config.venue_id,
                     name='spot',
                     url=self.config.base_url,
                     events=items)

    def sync_stores(self) -> Venue:
        spot_fetcher = SpotFetcher(self.config)
        spot_parser = SpotParser(self.config)

        data = spot_fetcher.fetch()
        events = spot_parser.parse(data)
        logging.info(f'fetched a total of {len(events)} items')
        self.event_repository.upsert(events)
        return self.create_venue(events)
