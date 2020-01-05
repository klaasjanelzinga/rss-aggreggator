import asyncio
import logging
from typing import Dict, List

from aiohttp import ClientSession, ClientTimeout
from google.cloud import datastore
import google.cloud.logging

from app.core.app_config import AppConfig
from app.core.event.event_entity_transformer import EventEntityTransformer
from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OC_TRACER, OpenCensusHelper
from app.core.user.user_profile_repository import UserProfileRepository
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.hedon_zwolle.hedon_processor import HedonProcessor
from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor
from app.venues.neushoorn_leeuwarden.neushoorn_processor import NeushoornProcessor
from app.venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor
from app.venues.paradiso_amsterdam.paradiso_processor import ParadisoProcessor
from app.venues.simplon_groningen.simplon_processor import SimplonProcessor
from app.venues.spot.spot_processor import SpotProcessor
from app.venues.t013_tilburg.t013_processor import T013Processor
from app.venues.tivoli_utrecht.tivoli_processor import TivoliProcessor
from app.venues.vera_groningen.vera_processor import VeraProcessor

if AppConfig.is_running_in_gae():
    LOGGING_CLIENT = google.cloud.logging.Client("rss-aggregator-236707")
    LOGGING_CLIENT.setup_logging(log_level=logging.INFO)
    LOGGING_CLIENT.get_default_handler().propagate = False
else:
    logging.basicConfig(level=logging.INFO)

# logging.basicConfig(level=logging.INFO)

DATASTORE_CLIENT = datastore.Client()
venue_repository: VenueRepository = VenueRepository()
event_entity_transformer: EventEntityTransformer = EventEntityTransformer(venue_repository=venue_repository)
event_repository: EventRepository = EventRepository(
    event_entity_transformer=event_entity_transformer, client=DATASTORE_CLIENT
)
user_profile_repository: UserProfileRepository = UserProfileRepository(client=DATASTORE_CLIENT)

OC_HELPER = OpenCensusHelper()

processors: List[VenueProcessor] = [
    SpotProcessor(event_repository, venue_repository, OC_HELPER),
    VeraProcessor(event_repository, venue_repository, OC_HELPER),
    ParadisoProcessor(event_repository, venue_repository, OC_HELPER),
    OostGroningenProcessor(event_repository, venue_repository, OC_HELPER),
    NeushoornProcessor(event_repository, venue_repository, OC_HELPER),
    T013Processor(event_repository, venue_repository, OC_HELPER),
    SimplonProcessor(event_repository, venue_repository, OC_HELPER),
    MelkwegProcessor(event_repository, venue_repository, OC_HELPER),
    TivoliProcessor(event_repository, venue_repository, OC_HELPER),
]
# Hedon does not have date fixing data. Exclude in the unit tests.
if AppConfig.is_running_in_gae():
    processors.append(HedonProcessor(event_repository, venue_repository, OC_HELPER))
processors_map: Dict[str, VenueProcessor] = {processor.venue.venue_id: processor for processor in processors}


async def async_venues(slices: int) -> None:
    timeout = ClientTimeout(40)
    venues_to_sync = processors[0:4] if slices == 0 else processors[4:]
    with OC_TRACER.span("async_venues"):
        async with ClientSession(timeout=timeout) as session:
            coroutines = [processor.fetch_new_events(session) for processor in venues_to_sync]
            await asyncio.gather(*coroutines)


def sync_venues(slices: int) -> None:
    asyncio.run(async_venues(slices))
