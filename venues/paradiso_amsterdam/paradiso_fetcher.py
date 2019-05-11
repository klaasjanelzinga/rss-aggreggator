from core.fetcher_util import FetcherUtil


class ParadisoFetcher:

    def __init__(self,
                 url='https://api.paradiso.nl/api/events?lang=en&start_time=now&sort=date&order=asc&limit=30&page={}&with=locations'):
        self.url = url

    def fetch(self, page_index: int) -> str:
        return FetcherUtil.fetch(self.url.format(page_index))
