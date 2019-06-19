from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.operators import flat_map

from app.core.source import Source
from app.core.venue import Venue
from app.venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TivoliSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str =
                 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand='):
        self.venue = venue
        self.scrape_url = scrape_url

    def tivoli_observer(self, observer: Observer, _) -> Observer:
        parser = TivoliParser()
        return Source.parse_page_indexed_observable(observer=observer, parser=parser, venue=self.venue,
                                                    scrape_url_format=self.scrape_url, items_per_page=30)

    def observable(self) -> Observable:
        return create(self.tivoli_observer).pipe(flat_map(from_iterable))
