from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.core.typing import Scheduler, Disposable
from rx.operators import flat_map

from app.core.fetcher_util import FetcherUtil
from app.core.parsing_context import ParsingContext
from app.core.source import Source
from app.venues.melkweg_amsterdam.melkweg_config import MelkwegConfig
from app.venues.melkweg_amsterdam.melkweg_parser import MelkwegParser


class MelkwegSource(Source):

    def __init__(self,
                 config: MelkwegConfig,
                 scrape_url: str = 'https://www.melkweg.nl/nl/agenda/as_json/1/grouped/0/page_size/-1?cb=2600605'):
        self.config = config
        self.venue = self.config.venue()
        self.scrape_url = scrape_url

    def melkweg_observer(self, observer: Observer, scheduler: Scheduler) -> Disposable:
        parser = MelkwegParser(self.config)
        data = FetcherUtil.fetch(self.scrape_url)
        observer.on_next(parser.parse(ParsingContext(venue=self.venue, content=data)))
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.melkweg_observer).pipe(flat_map(lambda events: from_iterable(events)))
