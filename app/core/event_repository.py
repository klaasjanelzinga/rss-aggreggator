import base64
from datetime import datetime
from typing import List, Optional

from google.cloud import datastore
from google.cloud.datastore import Entity
from google.cloud.datastore.client import Client
from google.cloud.datastore.query import Iterator

from app.core.datastore_utils import DatastoreUtils, QueryResult
from app.core.event import Event
from app.core.event_entity_transformer import EventEntityTransformer


class EventRepository:

    def __init__(self, event_entity_transformer: EventEntityTransformer, client: Client):
        self.client = client
        self.event_entity_transformer = event_entity_transformer

    def fetch_all_keys_as_string(self) -> List[str]:
        query = self.client.query(kind='Event')
        query.keys_only()
        return [key.key.name for key in list(query.fetch())]

    def _generate_entity(self, event: Event) -> Entity:
        entity = datastore.Entity(self.client.key('Event', event.event_id))
        entity.update(EventEntityTransformer.to_entity(event))
        return entity

    def upsert_no_slicing(self, events: List[Event]) -> List[Event]:
        self.client.put_multi([self._generate_entity(event) for event in set(events)])
        return events

    def fetch_items(self, cursor: Optional[bytes], limit: Optional[int]) -> QueryResult:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=cursor)
        if google_cursor is not None and google_cursor.decode('utf-8') == 'DONE':
            return QueryResult(items=[], token=base64.encodebytes('DONE'))
        query = self.client.query(kind='Event')
        query.order = ['when']

        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        return DatastoreUtils.construct_query_result_from_query(query_iter)

    def fetch_all_items(self) -> Iterator:
        query = self.client.query(kind='Event')
        query.order = ['when']
        return query.fetch()

    def search(self, term: str, cursor: Optional[bytes] = None, limit: Optional[int] = None) -> QueryResult:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=cursor)
        if google_cursor is not None and google_cursor.decode('utf-8') == 'DONE':
            return QueryResult(items=[], token=base64.encodebytes('DONE'))

        query = self.client.query(kind='Event')
        # pylint: disable=expression-not-assigned
        [query.add_filter('search_terms', '=', term) for term in DatastoreUtils.split_term(term)]
        query.order = ['when']
        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        return DatastoreUtils.construct_query_result_from_query(query_iter)

    def clean_items_before(self, date: datetime) -> int:
        query = self.client.query(kind='Event')
        query.add_filter('when', '<', date)
        query.keys_only()
        keys = [key.key for key in list(query.fetch())]
        self.client.delete_multi(keys)
        return len(keys)
