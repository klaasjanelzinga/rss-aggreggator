import unittest
from unittest.mock import Mock

from hamcrest import equal_to
from hamcrest.core import assert_that

from app.core.event_repository import EventRepository
from app.core.venue.venue_repository import VenueRepository
from app.venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor


class TestOostGroningenProcessor(unittest.TestCase):

    def setUp(self) -> None:
        self.event_repository = Mock(spec=EventRepository)
        self.venue_repository = Mock(spec=VenueRepository)
        self.processor = OostGroningenProcessor(event_repository=self.event_repository,
                                                venue_repository=self.venue_repository)

    def test_process_upserted_all_events(self):
        self.event_repository.upsert_no_slicing.return_value = []
        self.processor.sync_stores()
        self.event_repository.upsert_no_slicing.assert_called_once()
        args = self.event_repository.upsert_no_slicing.call_args[0][0]
        assert_that(len(args), equal_to(8))
