import unittest
from datetime import datetime
from unittest.mock import Mock

from hamcrest import equal_to, not_none
from hamcrest.core import assert_that

from core.event_entity_transformer import EventEntitytTransformer
from core.venue_repository import VenueRepository
from tests.core.fixtures import fixture_vera_venue, fixture_vera_event


class TestEventEntitytTransformer(unittest.TestCase):

    def setUp(self) -> None:
        self.venue_repository = Mock(spec=VenueRepository)
        self.event_entity_transformer = EventEntitytTransformer(self.venue_repository)
        self.venue_repository.get_venue_for.return_value = fixture_vera_venue()

    def test_mapping_to_event(self):
        event = self.event_entity_transformer.to_event(entity_map={
            'url': 'http://dummy',
            'description': 'test',
            'title': 'junit',
            'source': 'vera',
            'date_published': datetime.now(),
            'image_url': 'http://dd.jpg',
            'venue_id': 'vera',
            'when': datetime.now()
        })
        assert_that(event.url, equal_to('http://dummy'))
        assert_that(event.title, equal_to('junit'))
        assert_that(event.source, equal_to('vera'))
        assert_that(event.description, equal_to('test'))
        assert_that(event.image_url, equal_to('http://dd.jpg'))
        assert_that(event.venue, equal_to(fixture_vera_venue()))
        assert_that(event.when, not_none())
        self.venue_repository.get_venue_for.assert_called_once()
        self.venue_repository.get_venue_for.assert_called_with('vera')

    def test_mapping_to_entity(self):
        entity = EventEntitytTransformer.to_entity(fixture_vera_event())
        assert_that(entity['url'], fixture_vera_event().url)
        assert_that(entity['venue_id'], fixture_vera_event().venue.venue_id)
        assert_that(entity['image_url'], fixture_vera_event().image_url)
        assert_that(entity['source'], fixture_vera_event().source)
        assert_that(entity['when'], fixture_vera_event().when)
        assert_that(entity['description'], fixture_vera_event().description)
        assert_that(entity['title'], fixture_vera_event().title)
