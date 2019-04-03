import logging

from core.transformer import Transformer
from rss.channel_factory import ChannelFactory
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

channel = ChannelFactory.create_default_channel()
channel.add_items([Transformer.item_to_rss(item) for item in items])
channel.as_xml()
