from abc import ABC, abstractmethod


class VenueProcessor(ABC):

    @abstractmethod
    def sync_stores(self) -> None:
        pass
