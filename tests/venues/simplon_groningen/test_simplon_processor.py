import unittest
from unittest.mock import Mock

from hamcrest import equal_to
from hamcrest.core import assert_that

from core.event_repository import EventRepository
from core.venue_repository import VenueRepository
from venues.simplon_groningen.simplon_processor import SimplonProcessor


class TestSimplonProcessor(unittest.TestCase):

    def setUp(self) -> None:
        self.event_repository = Mock(spec=EventRepository)
        self.venue_repository = Mock(spec=VenueRepository)
        self.processor = SimplonProcessor(event_repository=self.event_repository, venue_repository=self.venue_repository)

    def test_process_upserted_all_events(self):
        self.event_repository.upsert_no_slicing.return_value = []
        self.processor.sync_stores()
        self.event_repository.upsert_no_slicing.assert_called_once()
        args = self.event_repository.upsert_no_slicing.call_args[0][0]
        assert_that(len(args), equal_to(29))
