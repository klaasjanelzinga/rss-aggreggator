from typing import List

from google.cloud import datastore
from google.cloud.datastore import Entity
from google.cloud.datastore.client import Client


from app.core.venue.venue import Venue
from app.core.venue.venue_entity_transformer import VenueEntityTransformer


class VenueRepository:
    def __init__(self, client: Client) -> None:
        self.client = client

    def _generate_entity(self, venue: Venue) -> Entity:
        entity = datastore.Entity(self.client.key("Venue", venue.venue_id))
        entity.update(VenueEntityTransformer.to_entity(venue))
        return entity

    def upsert(self, venue: Venue) -> Venue:
        self.client.put(self._generate_entity(venue))
        return venue

    def insert(self, venue: Venue) -> Venue:
        """ Only insert if venue does not yet exists. """
        key = self.client.key("Venue", venue.venue_id)
        if self.client.get(key) is None:
            self.upsert(venue)
        return venue

    def get_venue_for(self, venue_id: str) -> Venue:
        """ Fetch venue with id venue_id. Raises Exception if not found."""
        key = self.client.key("Venue", venue_id)
        data = self.client.get(key)
        if data is None:
            raise Exception(f"Venue with id {venue_id} not found.")
        return VenueEntityTransformer.to_venue(self.client.get(key))

    def fetch_all(self) -> List[Venue]:
        query = self.client.query(kind="Venue")
        return [VenueEntityTransformer.to_venue(entity) for entity in query.fetch()]
