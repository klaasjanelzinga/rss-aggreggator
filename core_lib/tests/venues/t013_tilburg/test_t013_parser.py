from datetime import datetime

from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that
import pytest

from core_lib.core.fetcher_util import fetch
from core_lib.core.parser import ParsingContext
from core_lib.venues.t013_tilburg import T013Parser, T013Processor


@pytest.mark.asyncio
async def test_sample_file(client_session: ClientSession):
    venue = T013Processor.create_venue()
    data = await fetch(session=client_session, url=venue.source_url)
    results = T013Parser().parse(ParsingContext(venue=venue, content=data))
    assert_that(results, is_not(none()))
    assert_that(len(results), equal_to(7))
    reunie = [item for item in results if item.url == "https://www.013.nl/programma/5423/snelle"]
    assert_that(len(reunie), equal_to(1))
    assert_that(reunie[0].source, equal_to(venue.source_url))
    assert_that(reunie[0].description, equal_to("Tot op de reu00fcnie!"))
    assert_that(reunie[0].date_published, is_not(none()))
    assert_that(
        reunie[0].image_url,
        equal_to("https://www.013.nl/uploads/cache/event_main_mobile/5d7febc5306f2.jpg?version=1568700682"),
    )
    assert_that(reunie[0].title, equal_to("Snelle + Pjotr"))
    assert_that(reunie[0].when, is_not(none()))
    assert_that(reunie[0].event_id, is_not(none()))
    assert_that(reunie[0].venue, equal_to(venue))

    for event in [r for r in results if r.when != datetime.min]:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))
        assert_that(event.image_url, is_not(none))
