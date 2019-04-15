from google.cloud import datastore

from core.event_repository import EventRepository
from core.venue_repository import VenueRepository

datastore_client = datastore.Client()
event_repository = EventRepository(datastore_client)
venue_repository = VenueRepository()


