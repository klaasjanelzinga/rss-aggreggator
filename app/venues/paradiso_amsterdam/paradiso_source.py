from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.operators import flat_map

from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.paradiso_amsterdam.paradiso_parser import ParadisoParser


class ParadisoSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://api.paradiso.nl/api/events'
                                   '?lang=en&start_time=now&sort=date&order=asc&limit=30&page={}&with=locations'):
        self.venue = venue
        self.scrape_url = scrape_url

    def paradiso_observer(self, observer: Observer, _) -> Observer:
        parser = ParadisoParser()
        return Source.parse_page_indexed_observable(observer=observer, parser=parser, venue=self.venue,
                                                    scrape_url_format=self.scrape_url, items_per_page=30)

    def observable(self) -> Observable:
        return create(self.paradiso_observer).pipe(flat_map(from_iterable))
