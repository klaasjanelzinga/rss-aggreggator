import asyncio
from datetime import datetime

import asynctest
from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to

from app.core.event.event import Event
from app.core.processing_chain.only_valid_events import OnlyValidEvents
from app.core.processing_chain.processing_chain import Chain, Link
from tests.core.fixtures import fixture_vera_event


class SinkMock(Link):
    def __init__(self):
        super().__init__()
        self.mocked = []

    async def chain(self, event: Event) -> None:
        print("mocking")
        self.mocked.append(event)


class TestEvent(asynctest.TestCase):
    async def setUp(self):
        self.sink = SinkMock()

    async def test_valid_event(self):
        chain = Chain([OnlyValidEvents(), self.sink])
        await chain.start_chain([fixture_vera_event()])

        assert_that(len(self.sink.mocked), equal_to(1))

    async def test_invalid_event(self):
        chain = Chain([OnlyValidEvents(), self.sink])
        event = fixture_vera_event()
        event.when = datetime.min
        await chain.start_chain([event])
        assert_that(len(self.sink.mocked), equal_to(0))
