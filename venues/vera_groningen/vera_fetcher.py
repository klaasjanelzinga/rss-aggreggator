from core.fetcher_util import FetcherUtil
from venues.vera_groningen.vera_config import VeraConfig


class VeraFetcher:

    def __init__(self, config: VeraConfig):
        self.url = config.scrape_url

    def fetch(self, page_index: int, items_per_page: int) -> str:
        url = self.url.format(page_index, items_per_page)
        return FetcherUtil.fetch(url)
