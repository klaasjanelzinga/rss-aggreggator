from abc import ABC, abstractmethod

from rx import Observable
from rx.core.typing import Observer

from app.core.fetcher_util import fetch
from app.core.parser import Parser
from app.core.parsing_context import ParsingContext
from app.core.venue import Venue


class Source(ABC):

    @abstractmethod
    def observable(self) -> Observable:
        pass

    @staticmethod
    def parse_all_at_once_observable(observer: Observer, parser: Parser, venue: Venue, scrape_url: str, ) -> Observer:
        data = fetch(scrape_url)
        events = parser.parse(ParsingContext(venue=venue, content=data))
        observer.on_next(events)
        observer.on_completed()
        return observer

    @staticmethod
    def parse_page_indexed_observable(
            observer: Observer,
            parser: Parser,
            venue: Venue,
            scrape_url_format: str,
            items_per_page: int) -> Observer:

        page_index = 0
        done = False

        while not done:
            page_index += 1
            data = fetch(scrape_url_format.format(page_index))
            new_events = parser.parse(ParsingContext(venue=venue, content=data))
            observer.on_next(new_events)
            done = len(new_events) < items_per_page
        observer.on_completed()
        return observer
