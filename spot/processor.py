import logging
from typing import List

from core.item import Event
from core.venue import Venue
from spot.config import SpotConfig
from spot.fetcher import SpotFetcher
from spot.parser import SpotParser


class SpotProcessor:

    def __init__(self):
        self.config = SpotConfig()

    def create_venue(self, items: List[Event]) -> Venue:
        return Venue(venue_id='spot-groningen', name='spot', url=self.config.base_url, items=items)

    def sync_stores(self) -> Venue:
        spot_fetcher = SpotFetcher(self.config)
        spot_parser = SpotParser(self.config)

        data = spot_fetcher.fetch()
        items = spot_parser.parse(data)
        logging.info(f'fetched a total of {len(items)} items')

        return self.create_venue(items)

    def dummy_items(self) -> Venue:
        with open('test/samples/spot/Programma - Spot Groningen.html') as f:
            content = ''.join(f.readlines())
            spot_parser = SpotParser(self.config)
            return self.create_venue(spot_parser.parse(content))

