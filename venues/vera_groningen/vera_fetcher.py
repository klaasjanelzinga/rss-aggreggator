from core.fetcher_util import FetcherUtil


class VeraFetcher:

    def __init__(self, scrape_url: str = 'https://www.vera-groningen.nl/wp/wp-admin/admin-ajax.php?action=renderProgramme&category=all&page={}&perpage={}&lang=nl'):
        self.url = scrape_url

    def fetch(self, page_index: int, items_per_page: int) -> str:
        url = self.url.format(page_index, items_per_page)
        return FetcherUtil.fetch(url)
