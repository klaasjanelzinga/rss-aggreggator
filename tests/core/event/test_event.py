import unittest
from datetime import datetime, timedelta

import pytz
from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from tests.core.fixtures import fixture_vera_event, fixture_vera_event_mock


class TestEvent(unittest.TestCase):
    def test_valid(self):
        assert_that(fixture_vera_event().is_valid(), equal_to(True))

    def test_title(self):
        event = fixture_vera_event()
        event.title = None
        assert_that(event.is_valid(), equal_to(False))
        event.title = ""
        assert_that(event.is_valid(), equal_to(False))

    def test_url(self):
        event = fixture_vera_event()
        event.url = None
        assert_that(event.is_valid(), equal_to(False))
        event.url = ""
        assert_that(event.is_valid(), equal_to(False))

    def test_description(self):
        event = fixture_vera_event()
        event.description = None
        assert_that(event.is_valid(), equal_to(False))
        event.description = ""
        assert_that(event.is_valid(), equal_to(False))

    def test_when(self):
        event = fixture_vera_event()
        event.when = datetime.min
        assert_that(event.is_valid(), equal_to(False))

    def test_equality(self):
        event = fixture_vera_event()
        event2 = fixture_vera_event()
        event3 = fixture_vera_event_mock()
        event3.url = "www.googlge"

        assert_that(event, equal_to(event2))
        assert_that(event2, equal_to(event))
        assert_that(event2, is_not(equal_to(event3)))
        assert_that(event, is_not(equal_to(event3)))

    def test_invalid_when_too_old(self):
        event = fixture_vera_event()
        event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) - timedelta(days=1)
        assert_that(event.is_valid(), equal_to(False))

        event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) - timedelta(minutes=1)
        assert_that(event.is_valid(), equal_to(False))

        event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) + timedelta(minutes=1)
        assert_that(event.is_valid(), equal_to(True))

    def test_invalid_event(self):
        event = fixture_vera_event()
        assert_that(event.is_valid(), equal_to(True))

        event = fixture_vera_event()
        event.title = None
        assert_that(event.is_valid(), equal_to(False))

        event = fixture_vera_event()
        event.image_url = None
        assert_that(event.is_valid(), equal_to(True))

        event = fixture_vera_event()
        event.description = None
        assert_that(event.is_valid(), equal_to(False))

        event = fixture_vera_event()
        event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) + timedelta(minutes=-1)
        assert_that(event.is_valid(), equal_to(False))
