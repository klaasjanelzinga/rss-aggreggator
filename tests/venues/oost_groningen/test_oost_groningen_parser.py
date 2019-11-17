import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.oost_groningen.oost_groningen_parser import OostGroningenParser
from app.venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor


class TestOostGroningenParser(asynctest.TestCase):
    async def setUp(self) -> None:
        self.session = ClientSession()

    async def tearDown(self) -> None:
        await self.session.close()

    async def test_parse(self):
        venue = OostGroningenProcessor.create_venue()
        content = await fetch(session=self.session, url=venue.url)
        results = OostGroningenParser().parse(ParsingContext(venue=venue, content=content))
        assert_that(len(results), equal_to(8))

        event = results[0]
        assert_that(event.title, equal_to("HOMOOST • Movie Night: Party Monster the Shockumentary"))
        assert_that(event.description, equal_to("Movie Screening • Group Discussion"))
        assert_that(event.when, is_not(none()))
        assert_that(event.url, equal_to("https://www.facebook.com/events/610421539383220/"))
        assert_that(
            event.image_url,
            equal_to("https://www.komoost.nl/media/56721601_1992667177522931_8267801960216788992_o.jpg"),
        )
        assert_that(event.venue, equal_to(venue))
        assert_that(event.source, equal_to("https://www.komoost.nl"))
        assert_that(event.event_id, is_not(none()))
        assert_that(event.date_published, is_not(none()))

        [assert_that(event.when, is_not(none)) for event in results]
        [assert_that(event.description, is_not(none())) for event in results]
        [assert_that(event.title, is_not(none())) for event in results]
        [assert_that(event.url, is_not(none())) for event in results]
