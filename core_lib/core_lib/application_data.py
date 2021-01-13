import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List

import pytz
from aiohttp import ClientSession, ClientTimeout
from google.cloud import datastore

from core_lib.core.repositories import VenueRepository, EventEntityTransformer, EventRepository
from core_lib.core.user_profile import UserProfileRepository
from core_lib.core.venue_processor import VenueProcessor
from core_lib.venues.hedon_zwolle import HedonProcessor
from core_lib.venues.melkweg_amsterdam import MelkwegProcessor
from core_lib.venues.neushoorn_leeuwarden import NeushoornProcessor
from core_lib.venues.oost_groningen import OostGroningenProcessor
from core_lib.venues.paradiso_amsterdam import ParadisoProcessor
from core_lib.venues.simplon_groningen import SimplonProcessor
from core_lib.venues.spot_groningen import SpotProcessor
from core_lib.venues.t013_tilburg import T013Processor
from core_lib.venues.tivoli_utrecht import TivoliProcessor
from core_lib.venues.vera_groningen import VeraProcessor

logging.basicConfig(level=logging.INFO)


# pylint: disable=C0103


class Repositories:
    @staticmethod
    def not_in_unit_tests() -> bool:
        return "unit_tests" not in os.environ

    def __init__(self) -> None:
        self.client = datastore.Client()
        self.venue_repository: VenueRepository = VenueRepository(client=self.client)
        self.event_entity_transformer: EventEntityTransformer = EventEntityTransformer(
            venue_repository=self.venue_repository
        )
        self.event_repository: EventRepository = EventRepository(
            event_entity_transformer=self.event_entity_transformer, client=self.client
        )
        self.user_profile_repository: UserProfileRepository = UserProfileRepository(client=self.client)
        self.timeout = ClientTimeout(total=60)

    def client_session(self) -> ClientSession:
        return ClientSession(timeout=self.timeout)


# pylint: disable=R0903
class Processors:
    def __init__(self, data_repositories: Repositories):
        self.venue_processors: List[VenueProcessor] = [
            SpotProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            VeraProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            ParadisoProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            OostGroningenProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            NeushoornProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            T013Processor(data_repositories.event_repository, data_repositories.venue_repository),
            SimplonProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            MelkwegProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            TivoliProcessor(data_repositories.event_repository, data_repositories.venue_repository),
            HedonProcessor(data_repositories.event_repository, data_repositories.venue_repository),
        ]

        # list as a venue_id -> venue dict.
        self.processors_map: Dict[str, VenueProcessor] = {
            processor.venue.venue_id: processor for processor in self.venue_processors
        }


repositories: Repositories = None  # type: ignore
venue_processors: Processors = None  # type: ignore
event_entity_transformer = None  # type: ignore
if Repositories.not_in_unit_tests():
    repositories = Repositories()
    venue_processors = Processors(repositories)
    event_entity_transformer = EventEntityTransformer(venue_repository=repositories.venue_repository)


async def _sync_these_processors(processors: List[VenueProcessor]) -> None:
    async with repositories.client_session() as client_session:
        coroutines = [processor.fetch_new_events(client_session) for processor in processors]
        await asyncio.gather(*coroutines)


async def _sync_these_processors_wrapper(processors: List[VenueProcessor]) -> None:
    await _sync_these_processors(processors)


async def async_venues(venues_before_utc: datetime, max_to_sync: int = 3) -> None:
    venues = [
        venue
        for venue in repositories.venue_repository.fetch_all()
        if venue.last_fetched_date < venue.convert_utc_to_venue_timezone(venues_before_utc)
    ]
    venues = sorted(venues, key=lambda v: v.last_fetched_date)
    await _sync_these_processors([venue_processors.processors_map[venue.venue_id] for venue in venues[:max_to_sync]])


def sync_venues() -> None:
    asyncio.run(async_venues(venues_before_utc=datetime.now(tz=pytz.utc) - timedelta(hours=20)))


def sync_all_venues() -> None:
    asyncio.run(async_venues(max_to_sync=99, venues_before_utc=datetime(9999, 1, 1, 1, 1, 1, 1, pytz.utc)))


def sync_integration_test_venues() -> None:
    asyncio.run(
        _sync_these_processors_wrapper(
            [
                venue_processors.processors_map["simplon-groningen"],
                venue_processors.processors_map["vera-groningen"],
                venue_processors.processors_map["spot-groningen"],
            ]
        )
    )
