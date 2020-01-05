from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from app.venues.vera_groningen.vera_processor import VeraProcessor
from app.venues.vera_groningen.vera_source import VeraSource


@pytest.mark.asyncio
async def test_sample_file(client_session: ClientSession):
    res = 0
    async for e in await VeraSource(VeraProcessor.create_venue()).fetch_events(session=client_session):
        res += len(e)
    assert_that(res, equal_to(34))
