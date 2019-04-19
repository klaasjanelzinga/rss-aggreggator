from datetime import datetime

from hamcrest import equal_to, not_none
from hamcrest.core import assert_that

from core.event import Event


class TestEvent:

    @staticmethod
    def fixture_event() -> Event:
        event = Event(url='http://dummy',
                      description='test',
                      title='junit',
                      source='vera',
                      date_published=datetime.now(),
                      image_url='http://dd.jpg',
                      venue_id='vera',
                      when=datetime.now())
        return event

    def test_valid(self):
        event = TestEvent.fixture_event()
        assert_that(event.is_valid(), equal_to(True))

        event = TestEvent.fixture_event()
        event.title = None
        assert_that(event.is_valid(), equal_to(False))
        event = TestEvent.fixture_event()
        event.title = ''

        event = TestEvent.fixture_event()
        event.url = None
        assert_that(event.is_valid(), equal_to(False))
        event = TestEvent.fixture_event()
        event.url = ''
        assert_that(event.is_valid(), equal_to(False))

        event = TestEvent.fixture_event()
        event.description = None
        assert_that(event.is_valid(), equal_to(False))
        event = TestEvent.fixture_event()
        event.description = ''
        assert_that(event.is_valid(), equal_to(False))

        event = TestEvent.fixture_event()
        event.when = datetime.min
        assert_that(event.is_valid(), equal_to(False))

    def test_mapping(self):
        event = Event.from_map({
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
        assert_that(event.venue_id, equal_to('vera'))
        assert_that(event.when, not_none())
