import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that

from app.core.fetcher_util import fetch
from app.core.parsing_context import ParsingContext
from app.venues.tivoli_utrecht.tivoli_parser import TivoliParser
from app.venues.tivoli_utrecht.tivoli_processor import TivoliProcessor


class TestTivoliParser(asynctest.TestCase):
    async def setUp(self) -> None:
        self.session = ClientSession()

    async def tearDown(self) -> None:
        await self.session.close()

    async def test_sample_file(self):
        venue = TivoliProcessor.create_venue()
        parser = TivoliParser()
        data = await fetch(session=self.session, url=f"{venue.url}/page=1")
        results = parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(len(results), equal_to(30))
        event = [result for result in results if result.title == "Worry Dolls"][0]

        assert_that(event.url, equal_to("https://www.tivolivredenburg.nl/agenda/worry-dolls-11-11-2019/"))
        assert_that(event.venue, equal_to(venue))
        assert_that(event.title, equal_to("Worry Dolls"))
        assert_that(event.when, is_not(none()))
        assert_that(
            event.image_url,
            equal_to("https://www.tivolivredenburg.nl/wp-content/uploads/2019/05/Duo-Print-195x130.jpg"),
        )
        assert_that(
            event.description, equal_to("Britse folk vol meerstemmige zang, banjo, ukulele, gitaar en mandoline")
        )
        assert_that(event.date_published, is_not(none()))
        assert_that(event.source, equal_to("https://www.tivolivredenburg.nl/agenda/"))

        for event in results:
            assert_that(event.when, is_not(none))
            assert_that(event.description, is_not(none))
            assert_that(event.title, is_not(none))
            assert_that(event.url, is_not(none))

    async def test_additional_event_data(self):
        venue = TivoliProcessor.create_venue()
        parser = TivoliParser()
        data = await fetch(session=self.session, url=f"{venue.url}/page=1")
        results = parser.parse(ParsingContext(venue=venue, content=data))
        assert_that(len(results), equal_to(30))
        event = [result for result in results if result.title == "Het Nieuwe Ouderschap"][0]
        assert_that(event.when.hour, equal_to(0))
        assert_that(event.when.hour, equal_to(0))
        event = parser.update_event_with_details(
            event=event, additional_details=await fetch(session=self.session, url=event.url)
        )
        assert_that(event.when.hour, equal_to(20))
        assert_that(event.when.minute, equal_to(15))
