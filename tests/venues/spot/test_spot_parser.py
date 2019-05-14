import unittest
from datetime import datetime
from hamcrest import is_not, none, equal_to
from hamcrest.core import assert_that

from core.parsing_context import ParsingContext
from tests.core.fixtures import fixture_vera_venue
from venues.spot.spot_config import SpotConfig
from venues.spot.spot_parser import SpotParser


class TestSpotParser(unittest.TestCase):

    def setUp(self):
        self.config = SpotConfig('http://junit-test', 'test_parser.py')
        self.parser = SpotParser(self.config)

    def test_sample_file(self):
        with open('tests/samples/spot/Programma - Spot Groningen.html') as f:
            results = self.parser.parse(ParsingContext(venue=fixture_vera_venue(), content=''.join(f.readlines())))
            assert_that(results, is_not(none()))
            assert_that(len(results), equal_to(58))
            kamagurka = [item for item in results if item.url == 'https://www.spotgroningen.nl/programma/kamagurka/']
            assert_that(len(kamagurka), equal_to(1))
            assert_that(kamagurka[0].source, equal_to('test_parser.py'))
            assert_that(kamagurka[0].description, equal_to('De overtreffende trap van absurditeit'))
            assert_that(kamagurka[0].date_published, is_not(none()))
            assert_that(kamagurka[0].image_url,
                        equal_to('http://junit-test/wp-content/uploads/2019/02/Kamagurka-20-20De-20grenzen-20van-20de-20ernst-20Kamagurka-202-20300-20dpi-20RGB-150x150.jpg'))
            assert_that(kamagurka[0].title, equal_to('Kamagurka - De grenzen van de ernst'))
            assert_that(kamagurka[0].when, equal_to(datetime.fromisoformat('2019-04-05T20:15:00+02:00')))
            assert_that(kamagurka[0].url, equal_to('https://www.spotgroningen.nl/programma/kamagurka/'))
            assert_that(kamagurka[0].id, is_not(none()))
            assert_that(kamagurka[0].venue, equal_to(fixture_vera_venue()))

            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]
