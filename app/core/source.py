from abc import ABC, abstractmethod

from rx import Observable


class Source(ABC):

    @abstractmethod
    def observable(self) -> Observable:
        pass
