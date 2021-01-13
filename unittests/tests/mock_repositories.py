import base64
import logging
import random
import re
from datetime import date, timedelta, datetime
from typing import Dict, List, Iterator, Optional
from unittest.mock import MagicMock, AsyncMock

from aiohttp import ClientSession
from google.cloud.datastore import Client

from core_lib.core.fetcher_util import setlocale
from core_lib.core.models import Event, Venue
from core_lib.core.repositories import QueryResult
from core_lib.core.user_profile import UserProfile

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__file__)


def url_to_id(url: str) -> str:
    return str(base64.encodebytes(bytes(url, "utf-8")), "utf-8")


class EventRepository:
    def __init__(self):
        self.store: Dict[str, Event] = {}

    def reset(self):
        self.store = {}

    def count(self) -> int:
        return len(self.store)

    def assert_events(self, venue):
        for event in self.store.values():
            assert event.when is not None
            assert event.description is not None
            assert event.title is not None
            assert event.url is not None
            assert event.event_id == url_to_id(event.url)
            assert event.date_published is not None
            assert event.venue.venue_id == venue.venue_id
            assert event.source == venue.source_url
            assert event.venue.last_fetched_date > venue.last_fetched_date

    def fetch_all_keys_as_string(self) -> List[str]:
        return [key for key in self.store.keys()]

    def fetch_all_keys_as_string_for_venue(self, venue: Venue) -> List[str]:
        return [event.event_id for event in self.store.values() if event.venue.venue_id == venue.venue_id]

    def upsert_no_slicing(self, events: List[Event]) -> List[Event]:
        for event in events:
            self.store[event.event_id] = event
        return events

    def fetch_items_on(self, when: date) -> QueryResult:
        raise Exception("Not implemented, yet")

    def fetch_items(self, cursor: Optional[bytes], limit: Optional[int]) -> QueryResult:
        raise Exception("Not implemented, yet")

    def fetch_all_rss_items(self) -> Iterator:
        return sorted(
            [event for event in self.store.values() if event.date_published > datetime.now() - timedelta(days=7)],
            key=lambda x: x.date_published,
        )

    def search(self, term: str, cursor: Optional[bytes] = None, limit: Optional[int] = None) -> QueryResult:
        raise Exception("Not implemented, yet")

    def clean_items_before(self, when: datetime) -> int:
        to_remove = len({(key, value) for key, value in self.store if value.when > when})
        self.store = {(key, value) for key, value in self.store if value.when > when}
        return to_remove


class VenueRepository:
    def __init__(self):
        self.store: Dict[str, Venue] = {}

    def reset(self):
        self.store = {}

    def upsert(self, venue: Venue) -> Venue:
        self.store[venue.venue_id] = venue
        return venue

    def insert(self, venue: Venue) -> Venue:
        """ Only insert if venue does not yet exists. """
        if venue.venue_id not in self.store:
            self.upsert(venue)
        return venue

    def get_venue_for(self, venue_id: str) -> Venue:
        """ Fetch venue with id venue_id. Raises Exception if not found."""
        if venue_id not in self.store:
            raise Exception(f"Venue with id {venue_id} not found.")
        return self.store[venue_id]

    def fetch_all(self) -> List[Venue]:
        return self.store.values()


class UserRepository:
    def __init__(self):
        self.store: Dict[str, UserProfile] = {}

    def reset(self):
        self.store = {}


class MockRepositories:
    def __init__(self):
        log.warning("Initializing MOCK repositories")
        self.user_repository = UserRepository()
        self.venue_repository = VenueRepository()
        self.event_repository = EventRepository()
        self.directory_for_mock_client_session = ""
        self.client = MagicMock(Client)

    @staticmethod
    def _fix(line: str) -> str:
        match = re.search(r"{{random_future_date:(.*?)}}", line)
        if match:
            date = datetime.now()
            increase = random.randint(2, 20)
            future_date = date + timedelta(days=increase)
            if match.groups()[0] == "timestamp":
                return re.sub(r"{{random_future_date:\w+}}", str(int(future_date.timestamp())), line)
            if match.groups()[0] == "tivoli":
                with setlocale("nl_NL.UTF-8"):
                    tivolies = (
                        f'"day": "{future_date.strftime("%a %-d")}", '
                        f'"month": "{future_date.strftime("%B")}", '
                        f'"year": "{future_date.strftime("%Y")}",'
                    )
                    return line.replace("{{random_future_date:tivoli}}", tivolies)
            if match.groups()[0] == "simplon-groningen":
                with setlocale("nl_NL.UTF-8"):
                    return line.replace(
                        "{{random_future_date:simplon-groningen}}", future_date.strftime("%a %-d %B %Y")
                    )
            if match.groups()[0] == "vera-groningen":
                with setlocale("nl_NL.UTF-8"):
                    return line.replace("{{random_future_date:vera-groningen}}", future_date.strftime("%A %-d %B"))
            if match.groups()[0] == "neushoorn-leeuwarden":
                with setlocale("nl_NL.UTF-8"):
                    return line.replace(
                        "{{random_future_date:neushoorn-leeuwarden}}", future_date.strftime("%A %-d %B")
                    )
            return re.sub(r"{{random_future_date:.*?}}", future_date.strftime(match.groups()[0]), line)
        return line

    def set_directory_for_mock_client_session(self, directory: str) -> None:
        self.directory_for_mock_client_session = directory

    def _mock_client_session_for_files(self) -> ClientSession:
        client_session_context_manager = AsyncMock()
        client_session = AsyncMock(ClientSession)

        def file_for_url(url: str) -> str:
            url = url.rstrip("/")
            last_part = url.rfind("/")
            file_name = (
                f"{self.directory_for_mock_client_session}/{url[last_part + 1:]}"
                if last_part > 8
                else f"{self.directory_for_mock_client_session}/index.html"
            )
            with open(file_name) as file:
                lines = file.readlines()

                def fix_a_line(line: str) -> str:
                    result = line
                    match = re.search(r"{{random_future_date:(.*?)}}", result)
                    while match:
                        result = MockRepositories._fix(result)
                        match = re.search(r"{{random_future_date:(.*?)}}", result)
                    return result

                return "".join([fix_a_line(line) for line in lines])

        def client_response(url: str):
            response = AsyncMock()
            text_await = AsyncMock()
            text_await.text.return_value = file_for_url(url)
            response.__aenter__.return_value = text_await
            return response

        client_session.get.side_effect = client_response
        client_session_context_manager.__aenter__.return_value = client_session
        return client_session_context_manager

    def client_session(self) -> ClientSession:
        return self._mock_client_session_for_files()

    def reset(self):
        self.user_repository.reset()
        self.venue_repository.reset()
        self.event_repository.reset()

        self.client.reset_mock()
