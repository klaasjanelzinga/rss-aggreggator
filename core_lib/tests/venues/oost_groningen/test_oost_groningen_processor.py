from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from core_lib.core.event.event_repository import EventRepository
from core_lib.venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor


@pytest.mark.asyncio
async def test_process_upserted_all_events(
    client_session: ClientSession, oost_processor: OostGroningenProcessor, mock_event_repository: EventRepository
):
    mock_event_repository.upsert_no_slicing.return_value = []
    mock_event_repository.fetch_all_keys_as_string_for_venue.return_value = []
    await oost_processor.fetch_new_events(session=client_session)
    mock_event_repository.upsert_no_slicing.assert_called_once()
    args = mock_event_repository.upsert_no_slicing.call_args[0][0]
    assert_that(len(args), equal_to(8))
