from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from app.core.event.event_repository import EventRepository
from app.venues.tivoli_utrecht.tivoli_processor import TivoliProcessor


@pytest.mark.asyncio
async def test_process_upserted_all_events(
    client_session: ClientSession, tivoli_processor: TivoliProcessor, mock_event_repository: EventRepository
):      
    mock_event_repository.upsert_no_slicing.return_value = []
    mock_event_repository.fetch_all_keys_as_string_for_venue.return_value = []
    total = await tivoli_processor.fetch_new_events(session=client_session)
    mock_event_repository.upsert_no_slicing.assert_called()
    args = mock_event_repository.upsert_no_slicing.call_args[0][0]
    assert_that(total, equal_to(37))
    assert_that(args[0].when.hour, equal_to(20))
    assert_that(args[0].description, equal_to("Mozart, Berg en Grieg"))
