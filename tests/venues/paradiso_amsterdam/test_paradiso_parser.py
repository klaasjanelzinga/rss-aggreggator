import unittest

from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from app.core.fetcher_util import FetcherUtil
from app.core.parsing_context import ParsingContext
from app.venues.paradiso_amsterdam.paradiso_config import ParadisoConfig
from app.venues.paradiso_amsterdam.paradiso_parser import ParadisoParser


class TestParadisoParser(unittest.TestCase):

    def test_sample_file_page_1(self):
        config = ParadisoConfig()
        parser = ParadisoParser(config)
        data = FetcherUtil.fetch(f'{config.source_url}/page=1')

        results = parser.parse(ParsingContext(venue=config.venue(), content=data))
        assert_that(len(results), equal_to(30))
        event = results[0]

        assert_that(event.url, equal_to('https://www.paradiso.nl/en/program/giant-rooks/54827'))
        assert_that(event.venue, equal_to(config.venue()))
        assert_that(event.title, equal_to("Giant Rooks"))
        assert_that(event.description, equal_to("Aanstormende Duitse indiepopband"))
        assert_that(event.when, is_not(none()))
        assert_that(event.image_url, none())
        assert_that(event.date_published, is_not(none()))
        assert_that(event.source, equal_to('https://www.paradiso.nl/'))

        [assert_that(event.when, is_not(none)) for event in results]
        [assert_that(event.description, is_not(none)) for event in results]
        [assert_that(event.title, is_not(none)) for event in results]
        [assert_that(event.url, is_not(none)) for event in results]

    def test_sample_file_page_2(self):
        config = ParadisoConfig()
        parser = ParadisoParser(config)
        data = FetcherUtil.fetch(f'{config.source_url}/page=2')

        results = parser.parse(ParsingContext(venue=config.venue(), content=data))
        assert_that(len(results), equal_to(1))

        [assert_that(event.when, is_not(none)) for event in results]
        [assert_that(event.description, is_not(none)) for event in results]
        [assert_that(event.title, is_not(none)) for event in results]
        [assert_that(event.url, is_not(none)) for event in results]

