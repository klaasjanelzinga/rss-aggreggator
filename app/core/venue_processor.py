import logging
from abc import ABC, abstractmethod

from rx.operators import filter as rx_filter, map as rx_map, buffer_with_count

from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue import Venue


class VenueProcessor(ABC):

    def __init__(self, event_repository: EventRepository, venue: Venue):
        self.event_repository = event_repository
        self.venue = venue
        self.logger = logging.getLogger(__name__)

    def sync_stores(self) -> None:
        self.fetch_source().observable().pipe(
            rx_filter(lambda event: event.is_valid()),
            buffer_with_count(200),
            rx_map(self.event_repository.upsert_no_slicing),
            rx_map(len),
        ).subscribe(
            on_next=lambda e: self.logger.info('Upserted %d events for %s', e, self.venue.venue_id),
            on_error=lambda e: self.logger.error('Error occurred syncing stores: %s', e),
        )

    @abstractmethod
    def fetch_source(self) -> Source:
        pass

    @staticmethod
    @abstractmethod
    def create_venue() -> Venue:
        pass
