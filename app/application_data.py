import logging
from typing import Dict, List

import google.cloud.logging
from google.cloud import datastore

from app.core.app_config import AppConfig
from app.core.event_entity_transformer import EventEntityTransformer
from app.core.event_repository import EventRepository
from app.core.user.user_profile_repository import UserProfileRepository
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor
from app.venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor
from app.venues.paradiso_amsterdam.paradiso_processor import ParadisoProcessor
from app.venues.simplon_groningen.simplon_processor import SimplonProcessor
from app.venues.spot.spot_processor import SpotProcessor
from app.venues.tivoli_utrecht.tivoli_processor import TivoliProcessor
from app.venues.vera_groningen.vera_processor import VeraProcessor

DATASTORE_CLIENT = datastore.Client()
venue_repository: VenueRepository = VenueRepository()
event_entity_transformer: EventEntityTransformer = EventEntityTransformer(venue_repository=venue_repository)
event_repository: EventRepository = EventRepository(event_entity_transformer=event_entity_transformer,
                                                    client=DATASTORE_CLIENT)
user_profile_repository: UserProfileRepository = UserProfileRepository(client=DATASTORE_CLIENT)

processors: List[VenueProcessor] = [
    SpotProcessor(event_repository, venue_repository),
    VeraProcessor(event_repository, venue_repository),
    OostGroningenProcessor(event_repository, venue_repository),
    SimplonProcessor(event_repository, venue_repository),
    ParadisoProcessor(event_repository, venue_repository),
    MelkwegProcessor(event_repository, venue_repository),
    TivoliProcessor(event_repository, venue_repository)
]
processors_map: Dict[str, VenueProcessor] = {processor.venue.venue_id: processor for processor in processors}

if AppConfig.is_running_in_gae():
    CLIENT = google.cloud.logging.Client('rss-aggregator-236707')
    CLIENT.setup_logging(log_level=logging.INFO)
    CLIENT.get_default_handler().propagate = False
else:
    logging.basicConfig(level=logging.INFO)
