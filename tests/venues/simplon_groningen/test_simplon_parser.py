import unittest
from datetime import datetime

from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from core.parsing_context import ParsingContext
from tests.core.fixtures import fixture_vera_venue
from venues.simplon_groningen.simplon_config import SimplonConfig
from venues.simplon_groningen.simplon_parser import SimplonParser


class TestSimplonParser(unittest.TestCase):

    def test_parse_sample(self):
        parser = SimplonParser(SimplonConfig(base_url='http://dumm'))
        with open('tests/samples/simplon-groningen/Simplon.html') as f:
            results = parser.parse(ParsingContext(venue=fixture_vera_venue(), content=''.join(f.readlines())))
            assert_that(len(results), equal_to(34))
            event = results[0]
            assert_that(event.title, equal_to('Foxlane + Car Pets'))
            assert_that(event.venue, equal_to(fixture_vera_venue()))
            assert_that(event.description, equal_to('Simplon UP'))
            assert_that(event.url, equal_to('http://simplon.nl/?post_type=events&p=17602'))
            assert_that(event.image_url,
                        equal_to('https://simplon.nl/content/uploads/2019/03/FOXLANE-MAIN-PRESS-PHOTO-600x600.jpg'))
            assert_that(event.when, equal_to(datetime.fromisoformat('2019-04-11T21:30:00+02:00')))
            assert_that(event.source, equal_to('http://dumm'))
            assert_that(event.date_published, is_not(none()))

            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]
