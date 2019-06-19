from rx import Observable, create, from_iterable
from rx.core import Observer
from rx.operators import flat_map

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.core.source import Source
from app.core.venue import Venue
from app.venues.melkweg_amsterdam.melkweg_parser import MelkwegParser


class MelkwegSource(Source):

    def __init__(self,
                 venue: Venue,
                 scrape_url: str = 'https://www.melkweg.nl/nl/agenda/as_json/1/grouped/0/page_size/-1?cb=2600605'):
        self.venue = venue
        self.scrape_url = scrape_url

    def melkweg_observer(self, observer: Observer, _) -> Observer:
        parser = MelkwegParser()
        data = fetch(self.scrape_url)
        observer.on_next(parser.parse(ParsingContext(venue=self.venue, content=data)))
        observer.on_completed()
        return observer

    def observable(self) -> Observable:
        return create(self.melkweg_observer).pipe(flat_map(from_iterable))
