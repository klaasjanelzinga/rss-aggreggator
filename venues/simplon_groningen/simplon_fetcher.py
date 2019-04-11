from core.fetcher_util import FetcherUtil


class SimplonFetcher:

    def __init__(self, scrape_url: str = 'https://www.simplon.nl'):
        self.url = scrape_url

    def fetch(self) -> str:
        return FetcherUtil.fetch(self.url)
