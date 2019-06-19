import unittest

from hamcrest import equal_to
from hamcrest.core import assert_that
from pytest import fail
from rx.operators import count

from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor
from app.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


class TestMelkwegAmsterdamSource(unittest.TestCase):

    def setUp(self) -> None:
        self.source = MelkwegSource(MelkwegProcessor.create_venue())

    def test_sample_file(self):
        self.source.observable().pipe(count()).subscribe(
            lambda aantal: assert_that(aantal, equal_to(46)),
            fail)
