from datetime import datetime

from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to
import pytest

from core_lib.core.event.event import Event
from core_lib.core.processing_chain.only_valid_events import OnlyValidEvents
from core_lib.core.processing_chain.processing_chain import Chain, Link


class SinkMock(Link):
    def __init__(self):
        super().__init__()
        self.mocked = []

    async def chain(self, event: Event) -> None:
        print("mocking")
        self.mocked.append(event)


@pytest.mark.asyncio
async def test_valid_event(valid_event: Event):
    sink = SinkMock()
    chain = Chain([OnlyValidEvents(), sink])
    await chain.start_chain([valid_event])

    assert_that(len(sink.mocked), equal_to(1))


@pytest.mark.asyncio
async def test_invalid_event(valid_event: Event):
    sink = SinkMock()
    chain = Chain([OnlyValidEvents(), sink])
    event = valid_event
    event.when = datetime.min
    await chain.start_chain([event])
    assert_that(len(sink.mocked), equal_to(0))
