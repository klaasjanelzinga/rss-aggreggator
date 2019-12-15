from unittest.mock import Mock

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from app.core.event.event_repository import EventRepository
from app.core.opencensus_util import OpenCensusHelper
from app.core.venue.venue_repository import VenueRepository
from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor


class TestMelkwegProcessor(asynctest.TestCase):
    async def tearDown(self) -> None:
        await self.session.close()

    async def setUp(self) -> None:
        self.session = ClientSession()
        self.event_repository = Mock(spec=EventRepository)
        self.venue_repository = Mock(spec=VenueRepository)
        self.oc_helper = Mock(spec=OpenCensusHelper)
        self.processor = MelkwegProcessor(
            event_repository=self.event_repository,
            venue_repository=self.venue_repository,
            open_census_helper=self.oc_helper,
        )

    async def test_process_upserted_all_events(self):
        self.event_repository.upsert_no_slicing.return_value = []
        await self.processor.fetch_new_events(session=self.session)
        self.event_repository.upsert_no_slicing.assert_called()
        args = self.event_repository.upsert_no_slicing.call_args[0][0]
        assert_that(len(args), equal_to(46))
