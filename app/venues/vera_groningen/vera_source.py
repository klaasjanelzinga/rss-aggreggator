from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.core.typing import Scheduler, Disposable
from rx.operators import flat_map

from app.core.fetcher_util import FetcherUtil
from app.core.parsing_context import ParsingContext
from app.core.source import Source
from app.venues.vera_groningen.vera_config import VeraConfig
from app.venues.vera_groningen.vera_parser import VeraParser


class VeraSource(Source):

    def __init__(self, config: VeraConfig,
                 scrape_url: str = 'https://www.vera-groningen.nl/wp/wp-admin/admin-ajax.php?'
                                   'action=renderProgramme&category=all&page={}&perpage={}&lang=nl'):
        self.config = config
        self.venue = self.config.venue()
        self.scrape_url = scrape_url

    def vera_observer(self, observer: Observer, scheduler: Scheduler) -> Disposable:
        vera_parser = VeraParser(self.config)
        items_per_page = 20
        page_index = 0
        done = False
        while not done:
            page_index += 1
            url = self.scrape_url.format(page_index, items_per_page)
            data = FetcherUtil.fetch(url)
            new_events = vera_parser.parse(ParsingContext(venue=self.venue, content=data))
            observer.on_next(new_events)
            done = len(new_events) < items_per_page
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.vera_observer).pipe(flat_map(lambda events: from_iterable(events)))
