import logging

from spot.config import SpotConfig
from spot.fetcher import SpotFetcher
from spot.parser import SpotParser

# init ...
logging.basicConfig(level=logging.INFO)

# execute daily ...
spot_config = SpotConfig()
spot_fetcher = SpotFetcher(spot_config)
spot_parser = SpotParser(spot_config)

data = spot_fetcher.fetch()
items = spot_parser.parse(data)
logging.info(f'fetched a total of {len(items)} items')
