from abc import ABC, abstractmethod
from typing import List

from core_lib.core.event.event import Event
from core_lib.core.parsing_context import ParsingContext


class Parser(ABC):
    @abstractmethod
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        pass

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        pass
