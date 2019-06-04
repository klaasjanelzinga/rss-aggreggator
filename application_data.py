import logging
from typing import Dict, List

import google.cloud.logging
from google.cloud import datastore

from core.app_config import AppConfig
from core.event_entity_transformer import EventEntityTransformer
from core.event_repository import EventRepository
from core.venue_processor import VenueProcessor
from core.venue_repository import VenueRepository
from venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor
from venues.paradiso_amsterdam.paradiso_processor import ParadisoProcessor
from venues.simplon_groningen.simplon_processor import SimplonProcessor
from venues.spot.spot_processor import SpotProcessor
from venues.tivoli_utrecht.tivoli_processor import TivoliProcessor
from venues.vera_groningen.vera_processor import VeraProcessor

datastore_client = datastore.Client()
venue_repository: VenueRepository = VenueRepository()
event_entity_transformer: EventEntityTransformer = EventEntityTransformer(venue_repository=venue_repository)
event_repository: EventRepository = EventRepository(event_entity_transformer=event_entity_transformer,
                                                    client=datastore_client)
processors: List[VenueProcessor] = [SpotProcessor(event_repository, venue_repository),
                                    VeraProcessor(event_repository, venue_repository),
                                    OostGroningenProcessor(event_repository, venue_repository),
                                    SimplonProcessor(event_repository, venue_repository),
                                    ParadisoProcessor(event_repository, venue_repository),
                                    TivoliProcessor(event_repository, venue_repository)]
processors_map: Dict[str, VenueProcessor] = {processor.venue.venue_id: processor for processor in processors}

if AppConfig.is_running_in_gae():
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=logging.INFO)
    client.get_default_handler().propagate = False
else:
    logging.basicConfig(level=logging.INFO)
