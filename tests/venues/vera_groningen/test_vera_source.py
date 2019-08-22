import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from app.venues.vera_groningen.vera_processor import VeraProcessor
from app.venues.vera_groningen.vera_source import VeraSource


class TestVeraGroningenSource(asynctest.TestCase):

    def setUp(self) -> None:
        self.source = VeraSource(VeraProcessor.create_venue())

    async def test_sample_file(self):
        res = 0
        async for e in await self.source.fetch_events(session=ClientSession()):
            res += len(e)
        assert_that(res, equal_to(34))
