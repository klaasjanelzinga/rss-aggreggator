import unittest
from unittest.mock import Mock

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from app.core.event_repository import EventRepository
from app.core.venue.venue_repository import VenueRepository
from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor


class TestMelkwegProcessor(asynctest.TestCase):

    def setUp(self) -> None:
        self.event_repository = Mock(spec=EventRepository)
        self.venue_repository = Mock(spec=VenueRepository)
        self.processor = MelkwegProcessor(event_repository=self.event_repository,
                                          venue_repository=self.venue_repository)

    async def test_process_upserted_all_events(self):
        self.event_repository.upsert_no_slicing.return_value = []
        await self.processor.async_store(session=ClientSession())
        self.event_repository.upsert_no_slicing.assert_called()
        args = self.event_repository.upsert_no_slicing.call_args[0][0]
        assert_that(len(args), equal_to(46))
