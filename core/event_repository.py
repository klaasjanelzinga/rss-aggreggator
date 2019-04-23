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

    @staticmethod
    def slice_it(batches: int, items: List) -> List[List]:
        result = []
        pivot = batches
        index = 0
        done = False
        while not done:
            actual = min(pivot+index, len(items))
            first = items[index:actual+index]
            done = actual == len(items)
            result.append(first)
            index += pivot
        return result

    def fetch_all_keys_as_string(self) -> List[str]:
        query = self.client.query(kind='Event')
        query.keys_only()
        return [key.key.name for key in list(query.fetch())]

    def _generate_entity(self, event: Event) -> Entity:
        entity = datastore.Entity(self.client.key('Event', event.id))
        entity.update(event.to_map())
        return entity

    def upsert(self, events: List[Event]) -> None:
        entities = [self._generate_entity(event) for event in set(events) if event.is_valid()]
        logging.info(f'Upserting {len(entities)} entities out of {len(events)} events')
        [self.client.put_multi(entities) for entities in EventRepository.slice_it(500, entities)]

    def fetch_items(self, cursor: bytes = None, limit: int = None) -> Tuple[List[Event], bytes]:
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
