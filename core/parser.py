from abc import ABC, abstractmethod
from typing import List

from core.event import Event


class Parser(ABC):

    @abstractmethod
    def parse(self, content: str) -> List[Event]:
        pass
