from core.fetcher_util import FetcherUtil
from spot.config import SpotConfig


class SpotFetcher:

    def __init__(self, config: SpotConfig):
        self.url = config.scrape_url

    def fetch(self) -> str:
        return FetcherUtil.fetch(self.url)
