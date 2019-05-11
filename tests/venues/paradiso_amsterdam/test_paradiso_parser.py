from datetime import datetime

from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from venues.paradiso_amsterdam.paradiso_config import ParadisoConfig
from venues.paradiso_amsterdam.paradiso_parser import ParadisoParser
from venues.tivoli_utrecht.tivoli_config import TivoliConfig
from venues.tivoli_utrecht.tivoli_parser import TivoliParser


class TestParadisoParser:

    def test_sample_file(self):
        parser = ParadisoParser(ParadisoConfig())
        with open('tests/samples/paradiso-amsterdam/ajax-1.js') as f:
            results = parser.parse(''.join(f.readlines()))
            assert_that(len(results), equal_to(30))
            event = results[0]

            assert_that(event.url,
                        equal_to('https://www.paradiso.nl/en/program/giant-rooks/54827'))
            assert_that(event.venue_id, equal_to('paradiso-amsterdam'))
            assert_that(event.title, equal_to("Giant Rooks"))
            assert_that(event.description, equal_to("Aanstormende Duitse indiepopband"))
            assert_that(event.when, equal_to(datetime.fromisoformat('2019-05-01T20:30:00+02:00')))
            assert_that(event.image_url, none())
            assert_that(event.date_published, is_not(none()))
            assert_that(event.source, equal_to('https://www.paradiso.nl/'))

            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]

