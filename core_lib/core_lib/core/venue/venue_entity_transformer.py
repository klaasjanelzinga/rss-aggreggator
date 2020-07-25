from typing import Dict

from core_lib.core.venue.venue import Venue


class VenueEntityTransformer:
    @staticmethod
    def to_entity(venue: Venue) -> Dict:
        return venue.__dict__

    @staticmethod
    def to_venue(entity: Dict) -> Venue:
        return Venue(**entity)
