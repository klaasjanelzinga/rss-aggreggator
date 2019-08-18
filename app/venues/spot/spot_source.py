from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.operators import flat_map

from app.core.source import Source
from app.core.venue.venue import Venue
from app.venues.spot.spot_parser import SpotParser


class SpotSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.spotgroningen.nl/programma'):
        self.venue = venue
        self.scrape_url = scrape_url

    def spot_observer(self, observer: Observer, _) -> Observer:
        parser = SpotParser()
        return Source.parse_all_at_once_observable(observer=observer, parser=parser,
                                                   venue=self.venue, scrape_url=self.scrape_url)

    def observable(self) -> Observable:
        return create(self.spot_observer).pipe(flat_map(from_iterable))
