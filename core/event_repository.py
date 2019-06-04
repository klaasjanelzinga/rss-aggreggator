import base64
import logging
from datetime import datetime
from typing import List, Tuple

from google.cloud import datastore
from google.cloud.datastore import Entity
from google.cloud.datastore.client import Client

from core.datastore_utils import DatastoreUtils
from core.event import Event
from core.event_entity_transformer import EventEntityTransformer


class EventRepository:

    def __init__(self, event_entity_transformer: EventEntityTransformer, client: Client):
        self.client = client
        self.event_entity_transformer = event_entity_transformer

    def fetch_all_keys_as_string(self) -> List[str]:
        query = self.client.query(kind='Event')
        query.keys_only()
        return [key.key.name for key in list(query.fetch())]

    def _generate_entity(self, event: Event) -> Entity:
        entity = datastore.Entity(self.client.key('Event', event.id))
        entity.update(EventEntityTransformer.to_entity(event))
        return entity

    def upsert(self, events: List[Event]) -> List[List[Event]]:
        entities = [self._generate_entity(event) for event in set(events) if event.is_valid()]
        logging.info(f'Upserting {len(entities)} entities out of {len(events)} events')
        return [self.client.put_multi(entities) for entities in DatastoreUtils.slice_it(500, entities)]

    def upsert_no_slicing(self, events: List[Event]) -> List[Event]:
        self.client.put_multi([self._generate_entity(event) for event in set(events)])
        return events

    def fetch_items(self, cursor: bytes = None, limit: int = None) -> Tuple[List[Event], bytes]:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=cursor)
        if google_cursor is not None and google_cursor.decode('utf-8') == 'DONE':
            return [], base64.encodebytes('DONE')
        query = self.client.query(kind='Event')
        query.order = ['when']

        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        results, next_cursor_encoded = DatastoreUtils.entities_and_cursor(query_iter)

        return [self.event_entity_transformer.to_event(entity) for entity in results], next_cursor_encoded

    def search(self, term: str, cursor: bytes = None, limit: int = None) -> Tuple[List[Event], bytes]:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=cursor)
        if google_cursor is not None and google_cursor.decode('utf-8') == 'DONE':
            return [], base64.encodebytes('DONE')

        query = self.client.query(kind='Event')
        [query.add_filter('search_terms', '=', term) for term in DatastoreUtils.split_term(term)]
        query.order = ['when']
        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        results, next_cursor_encoded = DatastoreUtils.entities_and_cursor(query_iter)

        return [self.event_entity_transformer.to_event(entity) for entity in results], next_cursor_encoded

    def clean_items_before(self, date: datetime) -> int:
        query = self.client.query(kind='Event')
        query.add_filter('when', '<', date)
        query.keys_only()
        keys = [key.key for key in list(query.fetch())]
        self.client.delete_multi(keys)
        return len(keys)
