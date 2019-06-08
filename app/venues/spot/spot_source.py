from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.core.typing import Scheduler, Disposable
from rx.operators import flat_map

from app.core.fetcher_util import FetcherUtil
from app.core.parsing_context import ParsingContext
from app.core.source import Source
from app.venues.spot.spot_config import SpotConfig
from app.venues.spot.spot_parser import SpotParser


class SpotSource(Source):

    def __init__(self,
                 config: SpotConfig,
                 scrape_url: str = 'https://www.spotgroningen.nl/programma'):
        self.config = config
        self.venue = self.config.venue()
        self.scrape_url = scrape_url

    def spot_observer(self, observer: Observer, scheduler: Scheduler) -> Disposable:
        parser = SpotParser(self.config)

        data = FetcherUtil.fetch(self.scrape_url)
        events = parser.parse(ParsingContext(venue=self.venue, content=data))
        observer.on_next(events)
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.spot_observer).pipe(flat_map(lambda events: from_iterable(events)))
