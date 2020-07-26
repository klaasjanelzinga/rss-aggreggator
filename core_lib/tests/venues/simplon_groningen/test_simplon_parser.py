from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that
import pytest

from core_lib.core.fetcher_util import fetch
from core_lib.core.parser import ParsingContext
from core_lib.venues.simplon_groningen import SimplonParser, SimplonProcessor


@pytest.mark.asyncio
async def test_parse_sample(client_session: ClientSession):
    venue = SimplonProcessor.create_venue()
    parser = SimplonParser()
    data = await fetch(session=client_session, url=venue.url)
    results = parser.parse(ParsingContext(venue=venue, content=data))
    assert_that(len(results), equal_to(29))
    event = results[0]
    assert_that(event.title, equal_to("Foxlane + Car Pets"))
    assert_that(event.venue, equal_to(venue))
    assert_that(event.description, equal_to("Simplon UP"))
    assert_that(event.url, equal_to("http://simplon.nl/?post_type=events&p=17602"))
    assert_that(
        event.image_url, equal_to("https://simplon.nl/content/uploads/2019/03/FOXLANE-MAIN-PRESS-PHOTO-600x600.jpg")
    )
    assert_that(event.when, is_not(none()))
    assert_that(event.source, equal_to("https://www.simplon.nl"))
    assert_that(event.date_published, is_not(none()))

    for event in results:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))
