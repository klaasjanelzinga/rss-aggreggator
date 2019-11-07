from unittest.mock import Mock

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from app.core.event.event_repository import EventRepository
from app.core.venue.venue_repository import VenueRepository
from app.venues.vera_groningen.vera_processor import VeraProcessor


class TestVeraGroningenProcessor(asynctest.TestCase):
    async def tearDown(self) -> None:
        await self.session.close()

    async def setUp(self) -> None:
        self.session = ClientSession()
        self.event_repository = Mock(spec=EventRepository)
        self.venue_repository = Mock(spec=VenueRepository)
        self.processor = VeraProcessor(event_repository=self.event_repository, venue_repository=self.venue_repository)

    async def test_process_upserted_all_events(self):
        self.event_repository.upsert_no_slicing.return_value = []
        result = await self.processor.fetch_new_events(session=self.session)
        self.event_repository.upsert_no_slicing.assert_called()
        assert_that(result, equal_to(34))
