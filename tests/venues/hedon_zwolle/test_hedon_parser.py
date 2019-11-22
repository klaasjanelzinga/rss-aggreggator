from datetime import datetime

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.hedon_zwolle.hedon_parser import HedonParser
from app.venues.hedon_zwolle.hedon_processor import HedonProcessor


class TestHedonParser(asynctest.TestCase):
    async def tearDown(self) -> None:
        await self.session.close()

    async def setUp(self):
        self.session = ClientSession()
        self.parser = HedonParser()

    async def test_sample_file(self):
        venue = HedonProcessor.create_venue()
        data = await fetch(session=self.session, url=venue.source_url)
        results = self.parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(results, is_not(none()))
        assert_that(len(results), equal_to(134))
        kamagurka = [item for item in results if item.url == "https://www.hedon-zwolle.nl/voorstelling/30294/zeroguap"]
        assert_that(len(kamagurka), equal_to(1))
        assert_that(kamagurka[0].source, equal_to(venue.source_url))
        assert_that(kamagurka[0].description, equal_to("ZEROGUAP"))
        assert_that(kamagurka[0].date_published, is_not(none()))
        assert_that(
            kamagurka[0].image_url,
            equal_to(
                "https://www.hedon-zwolle.nl/media/uploads/IMG_5155.jpg?width=400&height=400&ranchor=center&rmode=crop"
            ),
        )
        assert_that(kamagurka[0].title, equal_to("ZEROGUAP"))
        assert_that(kamagurka[0].when, is_not(none()))
        assert_that(kamagurka[0].event_id, is_not(none()))
        assert_that(kamagurka[0].venue, equal_to(venue))

        for event in [r for r in results if r.when != datetime.min]:
            assert_that(event.when, is_not(none))
            assert_that(event.description, is_not(none))
            assert_that(event.title, is_not(none))
            assert_that(event.url, is_not(none))
            assert_that(event.image_url, is_not(none))
