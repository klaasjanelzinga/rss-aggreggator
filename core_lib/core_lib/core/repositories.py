import base64
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

import pytz
from google.cloud import datastore
from google.cloud.datastore import Client, Entity
from google.cloud.datastore.query import Iterator
from pytz import timezone

from core_lib.core.models import Event, Venue, split_term


@dataclass
class QueryResult:
    items: Iterator
    token: bytes


class DatastoreUtils:
    @staticmethod
    def create_cursor(earlier_curor: Optional[bytes]) -> Optional[bytes]:
        return base64.decodebytes(earlier_curor) if earlier_curor is not None else None

    @staticmethod
    def construct_query_result_from_query(query_iter: Iterator) -> QueryResult:
        page = next(query_iter.pages)
        next_cursor = query_iter.next_page_token
        next_cursor_encoded = (
            base64.encodebytes(next_cursor) if next_cursor is not None else base64.encodebytes(bytes("DONE", "UTF-8"))
        )
        return QueryResult(items=page, token=next_cursor_encoded)


class VenueEntityTransformer:
    @staticmethod
    def to_entity(venue: Venue) -> Dict:
        return venue.__dict__

    @staticmethod
    def to_venue(entity: Dict) -> Venue:
        return Venue(**entity)


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


class EventEntityTransformer:
    def __init__(self, venue_repository: VenueRepository):
        self.venue_repository = venue_repository

    @staticmethod
    def to_entity(event: Event) -> Dict:
        return {
            "url": event.url,
            "title": event.title,
            "description": event.description,
            "venue_id": event.venue.venue_id,
            "source": event.source,
            "date_published": event.date_published,
            "when": event.when.astimezone(pytz.utc),
            "image_url": event.image_url,
            "search_terms": event.generate_search_terms(),
        }

    def to_event(self, entity_map: Dict) -> Event:
        venue_tz = timezone("Europe/Amsterdam")
        return Event(
            url=entity_map["url"],
            title=entity_map["title"],
            description=entity_map["description"],
            venue=self.venue_repository.get_venue_for(entity_map["venue_id"]),
            source=entity_map["source"],
            date_published=entity_map["date_published"],
            when=entity_map["when"].astimezone(venue_tz),
            image_url=entity_map["image_url"],
        )


class EventRepository:
    def __init__(self, event_entity_transformer: EventEntityTransformer, client: Client):
        self.client = client
        self.event_entity_transformer = event_entity_transformer

    def fetch_all_keys_as_string(self) -> List[str]:
        query = self.client.query(kind="Event")
        query.keys_only()
        return [key.key.name for key in list(query.fetch())]

    def fetch_all_keys_as_string_for_venue(self, venue: Venue) -> List[str]:
        query = self.client.query(kind="Event")
        query.add_filter("venue_id", "=", venue.venue_id)
        query.keys_only()
        return [key.key.name for key in list(query.fetch())]

    def _generate_entity(self, event: Event) -> Entity:
        entity = datastore.Entity(self.client.key("Event", event.event_id))
        entity.update(EventEntityTransformer.to_entity(event))
        return entity

    def upsert_no_slicing(self, events: List[Event]) -> List[Event]:
        self.client.put_multi([self._generate_entity(event) for event in set(events)])
        return events

    def fetch_items_on(self, when: date) -> QueryResult:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=None)
        query = self.client.query(kind="Event")
        query.add_filter("when", ">", datetime.combine(when, datetime.min.time()))
        query.add_filter("when", "<", datetime.combine(when, datetime.max.time()))
        query.order = ["when"]
        query_iter = query.fetch(start_cursor=google_cursor)
        return DatastoreUtils.construct_query_result_from_query(query_iter)

    def fetch_items(self, cursor: Optional[bytes], limit: Optional[int]) -> QueryResult:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=cursor)
        if google_cursor is not None and google_cursor.decode("utf-8") == "DONE":
            return QueryResult(items=iter([]), token=base64.encodebytes(b"DONE"))
        query = self.client.query(kind="Event")
        query.order = ["when"]

        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        return DatastoreUtils.construct_query_result_from_query(query_iter)

    def fetch_all_items(self) -> Iterator:
        query = self.client.query(kind="Event")
        query.order = ["when"]
        return query.fetch()

    def fetch_all_rss_items(self) -> Iterator:
        query = self.client.query(kind="Event")
        query.add_filter("date_published", ">", datetime.now() - timedelta(days=7))
        query.order = ["-date_published"]
        return query.fetch(limit=50)

    def search(self, term: str, cursor: Optional[bytes] = None, limit: Optional[int] = None) -> QueryResult:
        google_cursor = DatastoreUtils.create_cursor(earlier_curor=cursor)
        if google_cursor is not None and google_cursor.decode("utf-8") == "DONE":
            return QueryResult(items=iter([]), token=base64.encodebytes(b"DONE"))

        query = self.client.query(kind="Event")
        # pylint: disable=expression-not-assigned
        [query.add_filter("search_terms", "=", term) for term in split_term(term)]
        query.order = ["when"]
        query_iter = query.fetch(start_cursor=google_cursor, limit=limit)
        return DatastoreUtils.construct_query_result_from_query(query_iter)

    def clean_items_before(self, when: datetime) -> int:
        query = self.client.query(kind="Event")
        query.add_filter("when", "<", when)
        query.keys_only()
        keys = [key.key for key in list(query.fetch())]
        self.client.delete_multi(keys)
        return len(keys)
