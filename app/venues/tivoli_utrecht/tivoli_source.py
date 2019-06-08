from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.core.typing import Scheduler, Disposable
from rx.operators import flat_map

from app.core.fetcher_util import FetcherUtil
from app.core.parsing_context import ParsingContext
from app.core.source import Source
from app.venues.tivoli_utrecht.tivoli_config import TivoliConfig
from app.venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TivoliSource(Source):

    def __init__(self, config: TivoliConfig,
                 scrape_url: str =
                 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={}&categorie=&maand='):
        self.config = config
        self.venue = self.config.venue()
        self.scrape_url = scrape_url

    def tivoli_observer(self, observer: Observer, scheduler: Scheduler) -> Disposable:
        parser = TivoliParser(self.config)
        page_index = 0

        done = False
        while not done:
            page_index += 1
            data = FetcherUtil.fetch(self.scrape_url.format(page_index))
            new_events = parser.parse(ParsingContext(venue=self.venue, content=data))
            observer.on_next(new_events)
            done = len(new_events) < 30
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.tivoli_observer).pipe(flat_map(lambda events: from_iterable(events)))
