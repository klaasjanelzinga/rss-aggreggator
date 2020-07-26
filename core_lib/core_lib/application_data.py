import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List

import pytz
from aiohttp import ClientSession, ClientTimeout
from google.cloud import datastore

from core_lib.core.app_config import AppConfig
from core_lib.core.user_profile import UserProfileRepository
from core_lib.core.venue_processor import VenueProcessor
from core_lib.core.repositories import VenueRepository, EventEntityTransformer, EventRepository
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

DATASTORE_CLIENT = datastore.Client()
venue_repository: VenueRepository = VenueRepository(client=DATASTORE_CLIENT)
event_entity_transformer: EventEntityTransformer = EventEntityTransformer(venue_repository=venue_repository)
event_repository: EventRepository = EventRepository(
    event_entity_transformer=event_entity_transformer, client=DATASTORE_CLIENT
)
user_profile_repository: UserProfileRepository = UserProfileRepository(client=DATASTORE_CLIENT)

processors: List[VenueProcessor] = [
    SpotProcessor(event_repository, venue_repository),
    VeraProcessor(event_repository, venue_repository),
    ParadisoProcessor(event_repository, venue_repository),
    OostGroningenProcessor(event_repository, venue_repository),
    NeushoornProcessor(event_repository, venue_repository),
    T013Processor(event_repository, venue_repository),
    SimplonProcessor(event_repository, venue_repository),
    MelkwegProcessor(event_repository, venue_repository),
    TivoliProcessor(event_repository, venue_repository),
]
# Hedon does not have date fixing data. Exclude in the unit tests.
if AppConfig.is_production():
    processors.append(HedonProcessor(event_repository, venue_repository))
processors_map: Dict[str, VenueProcessor] = {processor.venue.venue_id: processor for processor in processors}


async def _sync_these_processors(procs: List[VenueProcessor]) -> None:
    timeout = ClientTimeout(40)
    async with ClientSession(timeout=timeout) as session:
        coroutines = [processor.fetch_new_events(session) for processor in procs]
        await asyncio.gather(*coroutines)


async def _sync_these_processors_wrapper(procs: List[VenueProcessor]) -> None:
    await _sync_these_processors(procs)


async def async_venues(venues_before_utc: datetime, max_to_sync: int = 3) -> None:
    venues = [
        venue
        for venue in venue_repository.fetch_all()
        if venue.last_fetched_date < venue.convert_utc_to_venue_timezone(venues_before_utc)
    ]
    venues = sorted(venues, key=lambda v: v.last_fetched_date)
    await _sync_these_processors([processors_map[venue.venue_id] for venue in venues[:max_to_sync]])


def sync_venues() -> None:
    asyncio.run(async_venues(venues_before_utc=datetime.now(tz=pytz.utc) - timedelta(hours=20)))


def sync_all_venues() -> None:
    asyncio.run(async_venues(max_to_sync=99, venues_before_utc=datetime(9999, 1, 1, 1, 1, 1, 1, pytz.utc)))


def sync_integration_test_venues() -> None:
    asyncio.run(
        _sync_these_processors_wrapper(
            [processors_map["simplon-groningen"], processors_map["vera-groningen"], processors_map["spot-groningen"]]
        )
    )
