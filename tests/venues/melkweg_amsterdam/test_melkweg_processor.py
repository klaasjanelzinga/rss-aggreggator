from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from app.core.event.event_repository import EventRepository
from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor


@pytest.mark.asyncio
async def test_process_upserted_all_events(
    client_session: ClientSession, melkweg_processor: MelkwegProcessor, mock_event_repository: EventRepository
):
    mock_event_repository.upsert_no_slicing.return_value = []
    await melkweg_processor.fetch_new_events(session=client_session)
    mock_event_repository.upsert_no_slicing.assert_called()
    args = mock_event_repository.upsert_no_slicing.call_args[0][0]
    assert_that(len(args), equal_to(46))
