import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor
from app.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


class TestMelkwegAmsterdamSource(asynctest.TestCase):

    def setUp(self) -> None:
        self.source = MelkwegSource(MelkwegProcessor.create_venue())

    async def test_sample_file(self):
        session = ClientSession()
        res = 0
        async for e in (await self.source.fetch_events(session=session)):
            res += len(e)
        assert_that(res, equal_to(46))
