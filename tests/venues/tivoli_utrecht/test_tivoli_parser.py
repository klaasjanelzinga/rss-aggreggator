import unittest

from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.tivoli_utrecht.tivoli_parser import TivoliParser
from app.venues.tivoli_utrecht.tivoli_processor import TivoliProcessor


class TestTivoliParser(unittest.TestCase):

    def test_sample_file(self):
        venue = TivoliProcessor.create_venue()
        parser = TivoliParser()
        data = fetch(f'{venue.url}/page=1')
        results = parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(len(results), equal_to(30))
        event = [result for result in results if result.title == "Leuk Dat Je d'r Bent Band"][0]

        assert_that(event.url,
                    equal_to('https://www.tivolivredenburg.nl/agenda/leuk-dat-je-dr-bent-band-27-04-2019/'))
        assert_that(event.venue, equal_to(venue))
        assert_that(event.title, equal_to("Leuk Dat Je d'r Bent Band"))
        assert_that(event.when, is_not(none()))
        assert_that(event.image_url, equal_to(
            'https://www.tivolivredenburg.nl/wp-content/uploads/2019/03/dezegebruikenleuk-195x130.jpg'))
        assert_that(event.description, equal_to("met EK '88 thema!"))
        assert_that(event.date_published, is_not(none()))
        assert_that(event.source, equal_to('https://www.tivolivredenburg.nl/agenda/'))

        for event in results:
            assert_that(event.when, is_not(none))
            assert_that(event.description, is_not(none))
            assert_that(event.title, is_not(none))
            assert_that(event.url, is_not(none))

