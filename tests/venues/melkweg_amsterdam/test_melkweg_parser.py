from datetime import datetime
import unittest

from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from app.core.fetcher_util import FetcherUtil
from app.core.parsing_context import ParsingContext
from app.venues.melkweg_amsterdam.melkweg_parser import MelkwegParser
from app.venues.melkweg_amsterdam.melkweg_config import MelkwegConfig


class TestMelkwegParser(unittest.TestCase):

    def test_parse(self):

        config = MelkwegConfig()
        with open('tests/samples/melkweg-amsterdam/-1.json') as f:
            content = ''.join(f.readlines())
            venue = config.venue()
            parser = MelkwegParser(config)
            results = parser.parse(ParsingContext(venue=venue, content=content))
            assert_that(len(results), equal_to(378))
            inna_event = [r for r in results if r.title == 'Inna de Yard feat. Horace Andy'][0]
            assert_that(inna_event.title, equal_to('Inna de Yard feat. Horace Andy'))
            assert_that(inna_event.description, equal_to(
                'Inna de Yard is het resultaat van een historische ontmoeting van twee generaties Jamaicaanse '
                'zangers en muzikanten tijdens traditionele akoestische jamsessies \'inna de yard\'. Levende legendes '
                'van de gouden jaren van de rootsreggae als Horace Andy, Ken Boothe en Cedric Myton werken samen met '
                'jong talent van het eiland en blazen zo de originele essentie van \'jamrock\' nieuw leven in. '
                'Na het succes van het eerste album in 2017 en enkele geweldige concerten in Parijs, is er nu een '
                'vervolg met een nieuw album en een film. De nieuwe tour is nu al legendarisch en gelukkig slaan '
                'ze Amsterdam niet over!\xa0'))
            assert_that(inna_event.image_url, equal_to(
                'https://s3-eu-west-1.amazonaws.com/static.melkweg.nl/uploads/images/scaled/agenda_thumbnail/25520'))
            assert_that(inna_event.source, equal_to('https://www.melkweg.nl/agenda'))
            assert_that(inna_event.url, equal_to('https://www.melkweg.nl/nl/agenda/inna-da-yard-13-06-2019'))
            assert_that(inna_event.when, equal_to(datetime.fromisoformat('2019-06-13T19:30:00+02:00')))

            for event in results:
                assert_that(event.title, is_not(none()))
                assert_that(event.description, is_not(none()))
                assert_that(event.image_url, is_not(none()))
                assert_that(event.source, is_not(none()))
                assert_that(event.when, is_not(none()))
                assert_that(event.url, is_not(none()))

    def test_small_sample(self):
        config = MelkwegConfig()
        data = FetcherUtil().fetch(config.source_url)
        events = MelkwegParser(config).parse(ParsingContext(config.venue(), data))
        assert_that(len(events), equal_to(46))

        for event in events:
            assert_that(event.title, is_not(none()))
            assert_that(event.description, is_not(none()))
            assert_that(event.image_url, is_not(none()))
            assert_that(event.source, is_not(none()))
            assert_that(event.when, is_not(none()))
            assert_that(event.url, is_not(none()))
            assert_that(event.is_valid(), equal_to(True))
