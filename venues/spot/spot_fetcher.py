from core.fetcher_util import FetcherUtil


class SpotFetcher:

    def __init__(self, scrape_url: str = 'https://www.spotgroningen.nl/programma'):
        self.url = scrape_url

    def fetch(self) -> str:
        return FetcherUtil.fetch(self.url)
