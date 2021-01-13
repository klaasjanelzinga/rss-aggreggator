from datetime import datetime

from hamcrest import equal_to, not_none
from hamcrest.core import assert_that

from core_lib.core.models import Event, Venue
from core_lib.core.repositories import VenueRepository, EventEntityTransformer


def test_mapping_to_entity(valid_event: Event):
    entity = EventEntityTransformer.to_entity(valid_event)
    assert_that(entity["url"], valid_event.url)
    assert_that(entity["venue_id"], valid_event.venue.venue_id)
    assert_that(entity["image_url"], valid_event.image_url)
    assert_that(entity["source"], valid_event.source)
    assert_that(entity["when"], valid_event.when)
    assert_that(entity["description"], valid_event.description)
    assert_that(entity["title"], valid_event.title)
    assert_that(len(entity), equal_to(9))
