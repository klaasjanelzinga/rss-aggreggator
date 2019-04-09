from typing import Dict, Tuple

from core.venue import Venue
from core.venue_processor import VenueProcessor


class VenueRepository:

    def __init__(self):
        self.registry: Dict[str, Tuple[Venue, VenueProcessor]] = {}

    def register(self, venue_id: str, venue: Venue, processor: VenueProcessor) -> Venue:
        self.registry[venue_id] = (venue, processor)
        return venue

    def get_processor(self, venue_id) -> VenueProcessor:
        if venue_id not in self.registry:
            raise Exception(f'Venue with id {venue_id} is not registered')
        return self.registry[venue_id][1]

    def get_venue_for(self, venue_id: str) -> Venue:
        return self.registry[venue_id][0]

    def sync_stores_for_venue(self, venue_id: str):
        self.get_processor(venue_id).sync_stores()

    def is_registered(self, venue_id) -> bool:
        return venue_id in self.registry
