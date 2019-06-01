import unittest
from datetime import datetime

from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that

from core.parsing_context import ParsingContext
from tests.core.fixtures import fixture_vera_venue
from venues.oost_groningen.oost_groningen_config import OostGroningenConfig
from venues.oost_groningen.oost_groningen_parser import OostGroningenParser


class TestOostGroningenParser(unittest.TestCase):

    def test_parse(self):
        config = OostGroningenConfig(base_url='http://dummy')
        with open('tests/samples/oost-groningen/komoost.html') as f:
            content = ''.join(f.readlines())
            results = OostGroningenParser(config).parse(ParsingContext(venue=fixture_vera_venue(), content=content))
            assert_that(len(results), equal_to(8))

            event = results[0]
            assert_that(event.title, equal_to('HOMOOST • Movie Night: Party Monster the Shockumentary'))
            assert_that(event.description, equal_to('Movie Screening • Group Discussion'))
            assert_that(event.when, equal_to(datetime.fromisoformat('2019-04-11T20:30:00+02:00')))
            assert_that(event.url, equal_to('https://www.facebook.com/events/610421539383220/'))
            assert_that(event.image_url,
                        equal_to('http://dummy/media/56721601_1992667177522931_8267801960216788992_o.jpg'))
            assert_that(event.venue, equal_to(fixture_vera_venue()))
            assert_that(event.source, equal_to('http://dummy'))
            assert_that(event.id, is_not(none()))
            assert_that(event.date_published, is_not(none()))

            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none())) for event in results]
            [assert_that(event.title, is_not(none())) for event in results]
            [assert_that(event.url, is_not(none())) for event in results]
