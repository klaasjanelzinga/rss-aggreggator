from copy import copy
from datetime import datetime, timedelta

import pytz
from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from core_lib.core.models import Event


def test_valid(valid_event: Event):
    assert_that(valid_event.is_valid(), equal_to(True))
    Event


def test_title(valid_event: Event):
    event = valid_event
    event.title = None
    assert_that(event.is_valid(), equal_to(False))
    event.title = ""
    assert_that(event.is_valid(), equal_to(False))


def test_url(valid_event: Event):
    event = valid_event
    event.url = None
    assert_that(event.is_valid(), equal_to(False))
    event.url = ""
    assert_that(event.is_valid(), equal_to(False))


def test_description(valid_event: Event):
    event = valid_event
    event.description = None
    assert_that(event.is_valid(), equal_to(False))
    event.description = ""
    assert_that(event.is_valid(), equal_to(False))


def test_when(valid_event: Event):
    event = valid_event
    event.when = datetime.min
    assert_that(event.is_valid(), equal_to(False))


def test_equality(valid_event: Event):
    event = valid_event
    event2 = copy(valid_event)
    event3 = copy(valid_event)
    event3.url = "www.googlge"
    event3.__post_init__()

    assert_that(event, equal_to(event2))
    assert_that(event2, equal_to(event))
    assert_that(event2, is_not(equal_to(event3)))
    assert_that(event, is_not(equal_to(event3)))


def test_invalid_when_too_old(valid_event: Event):
    event = valid_event
    event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) - timedelta(days=1)
    assert_that(event.is_valid(), equal_to(False))

    event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) - timedelta(minutes=1)
    assert_that(event.is_valid(), equal_to(False))

    event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) + timedelta(minutes=1)
    assert_that(event.is_valid(), equal_to(True))


def test_invalid_event_empty_title(valid_event: Event):
    event = valid_event
    assert_that(event.is_valid(), equal_to(True))

    event = valid_event
    event.title = None
    assert_that(event.is_valid(), equal_to(False))


def test_invalid_event_empty_image_url(valid_event: Event):
    event = valid_event
    event.image_url = None
    assert_that(event.is_valid(), equal_to(True))


def test_invalid_event_empty_description(valid_event: Event):
    event = valid_event
    event.description = None
    assert_that(event.is_valid(), equal_to(False))


def test_invalid_event_past_date(valid_event: Event):
    event = valid_event
    event.when = datetime.now(pytz.timezone("Europe/Amsterdam")) + timedelta(minutes=-1)
    assert_that(event.is_valid(), equal_to(False))
