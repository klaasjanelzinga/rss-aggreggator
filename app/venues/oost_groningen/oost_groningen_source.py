from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.operators import flat_map

from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.oost_groningen.oost_groningen_parser import OostGroningenParser


class OostGroningenSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.komoost.nl'):
        self.venue = venue
        self.scrape_url = scrape_url

    def oost_observer(self, observer: Observer, _) -> Observer:
        parser = OostGroningenParser()
        return Source.parse_all_at_once_observable(observer=observer, parser=parser, venue=self.venue,
                                                   scrape_url=self.scrape_url)

    def observable(self) -> Observable:
        return create(self.oost_observer).pipe(flat_map(from_iterable))
