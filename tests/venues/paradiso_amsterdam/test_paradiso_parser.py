import unittest

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.paradiso_amsterdam.paradiso_parser import ParadisoParser
from app.venues.paradiso_amsterdam.paradiso_processor import ParadisoProcessor


class TestParadisoParser(asynctest.TestCase):

    async def setUp(self) -> None:
        self.session = ClientSession()

    async def tearDown(self) -> None:
        await self.session.close()

    async def test_sample_file_page_1(self):
        venue = ParadisoProcessor.create_venue()
        parser = ParadisoParser()
        data = await fetch(session=self.session, url=f'{venue.source_url}/page=1')

        results = parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(len(results), equal_to(30))
        event = results[0]

        assert_that(event.url, equal_to('https://www.paradiso.nl/en/program/giant-rooks/54827'))
        assert_that(event.venue, equal_to(venue))
        assert_that(event.title, equal_to("Giant Rooks"))
        assert_that(event.description, equal_to("Aanstormende Duitse indiepopband"))
        assert_that(event.when, is_not(none()))
        assert_that(event.image_url, none())
        assert_that(event.date_published, is_not(none()))
        assert_that(event.source, equal_to('https://www.paradiso.nl/'))

        for event in results:
            assert_that(event.when, is_not(none))
            assert_that(event.description, is_not(none))
            assert_that(event.title, is_not(none))
            assert_that(event.url, is_not(none))

    async def test_sample_file_page_2(self):
        venue = ParadisoProcessor.create_venue()
        parser = ParadisoParser()
        data = await fetch(session=self.session, url=f'{venue.source_url}/page=2')

        results = parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(len(results), equal_to(1))

        for event in results:
            assert_that(event.when, is_not(none))
            assert_that(event.description, is_not(none))
            assert_that(event.title, is_not(none))
            assert_that(event.url, is_not(none))
