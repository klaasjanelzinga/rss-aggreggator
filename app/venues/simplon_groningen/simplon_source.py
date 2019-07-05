from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.core.typing import Disposable
from rx.operators import flat_map

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.core.source import Source
from app.core.venue import Venue
from app.venues.simplon_groningen.simplon_parser import SimplonParser


class SimplonSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.simplon.nl'):
        self.venue = venue
        self.scrape_url = scrape_url

    def simplon_observer(self, observer: Observer, _) -> Disposable:
        parser = SimplonParser()
        data = fetch(self.scrape_url)
        events = parser.parse(ParsingContext(venue=self.venue, content=data))

        observer.on_next(events)
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.simplon_observer).pipe(flat_map(from_iterable))
