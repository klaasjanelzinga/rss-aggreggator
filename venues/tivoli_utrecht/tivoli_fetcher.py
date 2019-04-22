from core.fetcher_util import FetcherUtil


class TivoliFetcher:

    def __init__(self,
                 scrape_url: str =
                 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand='):
        self.url = scrape_url

    def fetch(self, page_number: int) -> str:
        return FetcherUtil.fetch(self.url.format(page_number))
