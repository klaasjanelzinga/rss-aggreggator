import dateparser
from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from venues.vera_groningen.vera_config import VeraConfig
from venues.vera_groningen.vera_parser import VeraParser


class TestVeraGroningenParser:

    def test_sample_file(self):
        parser = VeraParser(VeraConfig())
        with open('tests/samples/vera-groningen/VERA Groningen - Programma.html') as f:
            results = parser.parse(''.join(f.readlines()))
            assert_that(len(results), equal_to(20))
            event = results[0]
            assert_that(event.url, equal_to('http://www.vera-groningen.nl/?post_type=events&p=99134&lang=nl'))
            assert_that(event.venue_id, equal_to('vera-groningen'))
            assert_that(event.title, equal_to('CLASH XXL Expo'))
            assert_that(event.when, equal_to(dateparser.parse('2019-04-07T14:00:00+02:00')))
            assert_that(event.image_url,
                        equal_to('https://www.vera-groningen.nl/content/uploads/2019/03/Sirene-Bouke-Groen-1-2-360x250.jpg'))
            assert_that(event.description, equal_to("CLASH XXL Expo with support BoukeGroen:Sirene+Lilnu'meVeen:SCHLÆGERCORE"))
            assert_that(event.date_published, is_not(none()))
            assert_that(event.source, equal_to('https://www.vera-groningen.nl/programma/'))

            event = results[2]
            assert_that(event.description, equal_to('Acusada'))
            assert_that(event.when, is_not(none()))
            assert_that(event.title, equal_to('Acusada (MOVIES THAT MATTER)'))

            event = results[3]
            assert_that(event.description, equal_to('Marissa Nadler (USA) with support Klaske Oenema (NL)'))
            assert_that(event.title, equal_to('Marissa Nadler (USA)'))

            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]

    def test_raw_fetches(self):
        parser = VeraParser(VeraConfig())
        with open('tests/samples/vera-groningen/raw-fetch-1.html') as f:
            results = parser.parse(''.join(f.readlines()))
            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]

        with open('tests/samples/vera-groningen/raw-fetch-2.html') as f:
            results = parser.parse(''.join(f.readlines()))
            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]

        with open('tests/samples/vera-groningen/raw-fetch-3.html') as f:
            results = parser.parse(''.join(f.readlines()))
            [assert_that(event.when, is_not(none)) for event in results]
            [assert_that(event.description, is_not(none)) for event in results]
            [assert_that(event.title, is_not(none)) for event in results]
            [assert_that(event.url, is_not(none)) for event in results]

