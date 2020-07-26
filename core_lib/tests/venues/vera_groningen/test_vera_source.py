from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from core_lib.venues.vera_groningen import VeraProcessor, VeraSource


@pytest.mark.asyncio
async def test_sample_file(client_session: ClientSession):
    res = 0
    async for e in await VeraSource(VeraProcessor.create_venue()).fetch_events(session=client_session):
        res += len(e)
    assert_that(res, equal_to(34))
