import logging
from abc import ABC

from rx.operators import filter, map, buffer_with_count

from core.event_repository import EventRepository
from core.source import Source
from core.venue import Venue
from core.venue_repository import VenueRepository


class VenueProcessor(ABC):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository, venue: Venue):
        self.event_repository = event_repository
        self.venue = venue
        venue_repository.register(self.venue)

    def sync_stores(self) -> None:
        self.fetch_source().observable().pipe(
            filter(lambda event: event.is_valid()),
            buffer_with_count(200),
            map(lambda events: self.event_repository.upsert_no_slicing(events)),
            map(lambda events: len(events)),
        ).subscribe(
            on_next=lambda e: logging.info(f'Upserted {e} events for {self.venue.venue_id}'),
            on_error=lambda e: print(f"Error Occurred: {e}"),
        )

    def fetch_source(self) -> Source:
        pass
