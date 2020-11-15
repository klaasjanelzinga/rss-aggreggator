from datetime import datetime

from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that
import pytest

from core_lib.core.fetcher_util import fetch
from core_lib.core.parser import ParsingContext
from core_lib.venues.hedon_zwolle import HedonParser, HedonProcessor


@pytest.mark.asyncio
async def test_sample_file(client_session: ClientSession):
    venue = HedonProcessor.create_venue()
    data = await fetch(session=client_session, url=venue.source_url)
    results = HedonParser().parse(ParsingContext(venue=venue, content=data))
    assert_that(results, is_not(none()))
    assert_that(len(results), equal_to(134))
    kamagurka = [item for item in results if item.url == "https://www.hedon-zwolle.nl/voorstelling/30294/zeroguap"]
    assert_that(len(kamagurka), equal_to(1))
    assert_that(kamagurka[0].source, equal_to(venue.source_url))
    assert_that(kamagurka[0].description, equal_to("ZEROGUAP"))
    assert_that(kamagurka[0].date_published, is_not(none()))
    assert_that(
        kamagurka[0].image_url,
        equal_to(
            "https://www.hedon-zwolle.nl/media/uploads/IMG_5155.jpg?width=400&height=400&ranchor=center&rmode=crop"
        ),
    )
    assert_that(kamagurka[0].title, equal_to("ZEROGUAP"))
    assert_that(kamagurka[0].when, is_not(none()))
    assert_that(kamagurka[0].event_id, is_not(none()))
    assert_that(kamagurka[0].venue, equal_to(venue))

    for event in [r for r in results if r.when is not None]:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))
        assert_that(event.image_url, is_not(none))
