from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
from hamcrest.core.core.isnone import not_none
import pytest

from core_lib.core.repositories import EventRepository
from core_lib.venues.paradiso_amsterdam import ParadisoProcessor


@pytest.mark.asyncio
async def test_process_upserted_all_events(
    client_session: ClientSession, paradiso_processor: ParadisoProcessor, mock_event_repository: EventRepository
):
    mock_event_repository.upsert_no_slicing.return_value = []
    mock_event_repository.fetch_all_keys_as_string_for_venue.return_value = []
    total = await paradiso_processor.fetch_new_events(session=client_session)
    mock_event_repository.upsert_no_slicing.assert_called()
    args = mock_event_repository.upsert_no_slicing.call_args[0][0]
    assert_that(total, equal_to(35))
    assert_that(args[0].image_url, not_none())
