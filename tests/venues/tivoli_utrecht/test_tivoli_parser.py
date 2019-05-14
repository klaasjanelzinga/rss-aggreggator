import unittest
from datetime import datetime

from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from core.parsing_context import ParsingContext
from tests.core.fixtures import fixture_vera_venue
from venues.tivoli_utrecht.tivoli_config import TivoliConfig
from venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TestTivoliParser(unittest.TestCase):

    def test_sample_file(self):
        parser = TivoliParser(TivoliConfig())
        with open('tests/samples/tivoli-utrecht/ajax-1.js') as f:
            results = parser.parse(ParsingContext(venue=fixture_vera_venue(), content=''.join(f.readlines())))
            assert_that(len(results), equal_to(30))
            event = [result for result in results if result.title == "Leuk Dat Je d'r Bent Band"][0]

            assert_that(event.url,
                        equal_to('https://www.tivolivredenburg.nl/agenda/leuk-dat-je-dr-bent-band-27-04-2019/'))
            assert_that(event.venue, equal_to(fixture_vera_venue()))
            assert_that(event.title, equal_to("Leuk Dat Je d'r Bent Band"))
            assert_that(event.when, equal_to(datetime.fromisoformat('2019-04-27T00:00:00+02:00')))
            assert_that(event.image_url, equal_to(
                'https://www.tivolivredenburg.nl/wp-content/uploads/2019/03/dezegebruikenleuk-195x130.jpg'))
            assert_that(event.description, equal_to("met EK '88 thema!"))
            assert_that(event.date_published, is_not(none()))
            assert_that(event.source, equal_to('https://www.tivolivredenburg.nl/agenda/'))

            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]

