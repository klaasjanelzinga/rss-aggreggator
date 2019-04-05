import logging
from datetime import datetime
from typing import List

from google.cloud import datastore
from google.cloud.datastore import Entity
from google.cloud.datastore.client import Client

from core.event import Event


class EventRepository:

    def __init__(self, client: Client):
        self.client = client

    def fetch_all_keys_as_string(self) -> List[str]:
        query = self.client.query(kind='Event')
        query.keys_only()
        return [key.key.name for key in list(query.fetch())]

    def _generate_entity(self, event: Event) -> Entity:
        entity = datastore.Entity(self.client.key('Event', event.id))
        entity.update(event.to_map())
        return entity

    def insert_new_events(self, events: List[Event]) -> None:
        current_keys = self.fetch_all_keys_as_string()
        updatable_events = [event for event in events if event.id not in current_keys]
        entities = [self._generate_entity(event) for event in updatable_events]
        logging.info(f'Inserting {len(entities)} new events out of {len(events)} events')
        self.client.put_multi(entities)

    def upsert(self, events: List[Event]) -> None:
        entities = [self._generate_entity(event) for event in events]
        logging.info(f'Upserting {len(entities)} new events out of {len(events)} events')
        self.client.put_multi(entities)

    def fetch_items(self) -> List[Event]:
        query = self.client.query(kind='Event')
        query.order = ['-when']
        results = list(query.fetch())
        return [Event.from_map(entity) for entity in results]

    def clean_items_before(self, date: datetime) -> int:
        query = self.client.query(kind='Event')
        query.add_filter('when', '<', date)
        query.keys_only()
        keys = [key for key in list(query.fetch())]
        self.client.delete_multi(keys)
        return len(keys)
