from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest

from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor
from app.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


@pytest.mark.asyncio
async def test_sample_file(client_session: ClientSession):
    source = MelkwegSource(MelkwegProcessor.create_venue())
    res = 0
    async for e in (await source.fetch_events(session=client_session)):
        res += len(e)
    assert_that(res, equal_to(46))
