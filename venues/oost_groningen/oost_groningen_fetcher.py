from core.fetcher_util import FetcherUtil


class OostGroningenFetcher:

    def __init__(self, scrape_url: str = 'https://www.komoost.nl'):
        self.url = scrape_url

    def fetch(self) -> str:
        return FetcherUtil.fetch(self.url)
