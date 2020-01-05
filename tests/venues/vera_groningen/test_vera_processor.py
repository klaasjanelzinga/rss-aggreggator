from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from app.core.event.event_repository import EventRepository
from app.venues.vera_groningen.vera_processor import VeraProcessor


@pytest.mark.asyncio
async def test_process_upserted_all_events(
    client_session: ClientSession, vera_processor: VeraProcessor, mock_event_repository: EventRepository
): 
    mock_event_repository.upsert_no_slicing.return_value = []
    result = await vera_processor.fetch_new_events(session=client_session)
    mock_event_repository.upsert_no_slicing.assert_called()
    assert_that(result, equal_to(34))
