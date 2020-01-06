from datetime import datetime

from hamcrest import equal_to, not_none
from hamcrest.core import assert_that

from app.core.event.event import Event
from app.core.event.event_entity_transformer import EventEntityTransformer
from app.core.venue.venue import Venue
from app.core.venue.venue_repository import VenueRepository


def test_mapping_to_event(mock_venue_repository: VenueRepository, valid_venue: Venue):
    event_entity_transformer = EventEntityTransformer(mock_venue_repository)
    mock_venue_repository.get_venue_for.return_value = valid_venue
    event = event_entity_transformer.to_event(
        entity_map={
            "url": "http://dummy",
            "description": "test",
            "title": "junit",
            "source": "vera",
            "date_published": datetime.now(),
            "image_url": "http://dd.jpg",
            "venue_id": valid_venue.venue_id,
            "when": datetime.now(),
        }
    )
    assert_that(event.url, equal_to("http://dummy"))
    assert_that(event.title, equal_to("junit"))
    assert_that(event.source, equal_to("vera"))
    assert_that(event.description, equal_to("test"))
    assert_that(event.image_url, equal_to("http://dd.jpg"))
    assert_that(event.venue, equal_to(valid_venue))
    assert_that(event.when, not_none())
    mock_venue_repository.get_venue_for.assert_called_once()
    mock_venue_repository.get_venue_for.assert_called_with(valid_venue.venue_id)

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
