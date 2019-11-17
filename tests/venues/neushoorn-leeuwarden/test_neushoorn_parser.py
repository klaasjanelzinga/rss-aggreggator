import asynctest
from aiohttp import ClientSession
from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.neushoorn_leeuwarden.neushoorn_parser import NeushoornParser
from app.venues.neushoorn_leeuwarden.neushoorn_processor import NeushoornProcessor


class TestNeushoornParser(asynctest.TestCase):
    async def setUp(self) -> None:
        self.session = ClientSession()

    async def tearDown(self) -> None:
        await self.session.close()

    async def test_parse(self):
        venue = NeushoornProcessor.create_venue()
        content = await fetch(session=self.session, url="https://neushoorn.nl/upcoming_events")
        results = NeushoornParser().parse(ParsingContext(venue=venue, content=content))
        assert_that(len(results), equal_to(16))

        result = [r for r in results if r.title == "Uit de Hoge Hoed: Improv Comedy"][0]
        assert_that(result.url, equal_to("https://neushoorn.nl/production/uit-de-hoge-hoed-improv-comedy-11/"))
        assert (
            "November 21, 2019 in Leeuwarden. Met Uit de Hoge Hoed lig je gegarandeerd de hele avond in een deuk! "
            in result.description
        )

    async def test_parse_details(self):
        venue = NeushoornProcessor.create_venue()
        content = await fetch(session=self.session, url="https://neushoorn.nl/upcoming_events")
        results = NeushoornParser().parse(ParsingContext(venue=venue, content=content))
        assert_that(len(results), equal_to(16))

        event = [r for r in results if r.title == "Uit de Hoge Hoed: Improv Comedy"][0]
        content = await fetch(session=self.session, url=event.url)
        event = NeushoornParser().update_event_with_details(event, content)

        assert event is not None
        assert event.when is not None
        assert (
            event.image_url == "https://neushoorn.nl/wp-content/uploads/2019/06/uit_de_hoge_hoed_front-2-1024x576.jpg"
        )
