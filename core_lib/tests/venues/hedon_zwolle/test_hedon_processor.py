from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from core_lib.core.repositories import EventRepository
from core_lib.venues.hedon_zwolle import HedonProcessor


@pytest.mark.asyncio
async def test_process_upserted_all_events(
    client_session: ClientSession, hedon_processor: HedonProcessor, mock_event_repository: EventRepository
):
    mock_event_repository.upsert_no_slicing.return_value = []
    await hedon_processor.fetch_new_events(session=client_session)
    mock_event_repository.upsert_no_slicing.assert_called_once()
    args = mock_event_repository.upsert_no_slicing.call_args[0][0]
    assert_that(len(args), equal_to(132))
