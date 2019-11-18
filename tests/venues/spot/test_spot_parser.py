import unittest

import asynctest
from aiohttp import ClientSession
from hamcrest import is_not, none, equal_to
from hamcrest.core import assert_that

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.spot.spot_parser import SpotParser
from app.venues.spot.spot_processor import SpotProcessor


class TestSpotParser(asynctest.TestCase):
    async def tearDown(self) -> None:
        await self.session.close()

    async def setUp(self):
        self.session = ClientSession()
        self.parser = SpotParser()

    async def test_sample_file(self):
        venue = SpotProcessor.create_venue()
        data = await fetch(session=self.session, url=venue.url)
        results = self.parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(results, is_not(none()))
        assert_that(len(results), equal_to(20))
        kamagurka = [item for item in results if item.url == "https://www.spotgroningen.nl/programma/kamagurka/"]
        assert_that(len(kamagurka), equal_to(1))
        assert_that(kamagurka[0].source, equal_to("https://www.spotgroningen.nl/programma"))
        assert_that(kamagurka[0].description, equal_to("De overtreffende trap van absurditeit"))
        assert_that(kamagurka[0].date_published, is_not(none()))
        assert_that(
            kamagurka[0].image_url,
            equal_to(
                "https://www.spotgroningen.nl/wp-content/uploads/2019/02/"
                "Kamagurka-20-20De-20grenzen-20van-20de-20ernst-20"
                "Kamagurka-202-20300-20dpi-20RGB-150x150.jpg"
            ),
        )
        assert_that(kamagurka[0].title, equal_to("Kamagurka - De grenzen van de ernst"))
        assert_that(kamagurka[0].when, is_not(none()))
        assert_that(kamagurka[0].url, equal_to("https://www.spotgroningen.nl/programma/kamagurka/"))
        assert_that(kamagurka[0].event_id, is_not(none()))
        assert_that(kamagurka[0].venue, equal_to(venue))

        for event in results:
            assert_that(event.when, is_not(none))
            assert_that(event.description, is_not(none))
            assert_that(event.title, is_not(none))
            assert_that(event.url, is_not(none))
