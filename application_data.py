import logging

import google.cloud.logging
from google.cloud import datastore

from core.app_config import AppConfig
from core.event_entity_transformer import EventEntitytTransformer
from core.event_repository import EventRepository
from core.venue_repository import VenueRepository

datastore_client = datastore.Client()
venue_repository = VenueRepository()
event_entity_transformer = EventEntitytTransformer(venue_repository=venue_repository)
event_repository = EventRepository(event_entity_transformer=event_entity_transformer, client=datastore_client)

if AppConfig.is_running_in_gae():
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=logging.INFO)
    client.get_default_handler().propagate = False
else:
    logging.basicConfig(level=logging.INFO)
