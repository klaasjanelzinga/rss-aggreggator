from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.core.typing import Scheduler, Disposable
from rx.operators import flat_map

from core.fetcher_util import FetcherUtil
from core.parsing_context import ParsingContext
from core.source import Source
from venues.oost_groningen.oost_groningen_config import OostGroningenConfig
from venues.oost_groningen.oost_groningen_parser import OostGroningenParser


class OostGroningenSource(Source):

    def __init__(self,
                 config: OostGroningenConfig,
                 scrape_url: str = 'https://www.komoost.nl'):
        self.config = config
        self.venue = self.config.venue()
        self.scrape_url = scrape_url

    def oost_observer(self, observer: Observer, scheduler: Scheduler) -> Disposable:
        parser = OostGroningenParser(self.config)
        data = FetcherUtil.fetch(self.scrape_url)
        events = parser.parse(ParsingContext(venue=self.venue, content=data))
        observer.on_next(events)
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.oost_observer).pipe(flat_map(lambda events: from_iterable(events)))
