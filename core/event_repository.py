import base64
import logging
from datetime import datetime
from google.cloud import datastore
from google.cloud.datastore import Entity
from google.cloud.datastore.client import Client
from typing import List, Tuple

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
        updatable_events = [event for event in events if event.id not in current_keys and event.is_valid()]
        entities = [self._generate_entity(event) for event in updatable_events]
        logging.info(f'Inserting {len(entities)} new events out of {len(events)} events')
        self.client.put_multi(entities)

    def upsert(self, events: List[Event]) -> None:
        entities = [self._generate_entity(event) for event in events if event.is_valid()]
        logging.info(f'Upserting {len(entities)} new events out of {len(events)} events')
        self.client.put_multi(entities)

    def fetch_items(self, cursor: bytes = None, limit: int = 0) -> Tuple[List[Event], bytes]:
        google_cursor = base64.decodebytes(cursor) if cursor is not None else None
        if google_cursor is not None and google_cursor.decode('utf-8') == 'DONE':
            return [], base64.encodebytes('DONE')
        query = self.client.query(kind='Event')
        query.order = ['when']

        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        page = next(query_iter.pages)
        results = list(page)
        next_cursor = query_iter.next_page_token
        next_cursor_encoded = base64.encodebytes(next_cursor) if next_cursor is not None \
            else base64.encodebytes(bytes('DONE', 'UTF-8'))

        return [Event.from_map(entity) for entity in results], next_cursor_encoded

    def clean_items_before(self, date: datetime) -> int:
        query = self.client.query(kind='Event')
        query.add_filter('when', '<', date)
        query.keys_only()
        keys = [key.key for key in list(query.fetch())]
        self.client.delete_multi(keys)
        return len(keys)
