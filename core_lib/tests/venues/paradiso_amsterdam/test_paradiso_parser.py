from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that
import pytest

from core_lib.core.fetcher_util import fetch
from core_lib.core.parser import ParsingContext
from core_lib.venues.paradiso_amsterdam import ParadisoParser, ParadisoProcessor


@pytest.mark.asyncio
async def test_sample_file_page_1(client_session: ClientSession):
    venue = ParadisoProcessor.create_venue()
    parser = ParadisoParser()
    data = await fetch(session=client_session, url=f"{venue.source_url}/page=1")

    results = parser.parse(ParsingContext(venue=venue, content=data))
    assert_that(len(results), equal_to(30))
    event = results[0]

    assert_that(event.url, equal_to("https://api.paradiso.nl/api/library/lists/events/60445?lang=en"))
    assert_that(event.venue, equal_to(venue))
    assert_that(event.title, equal_to("CROPFEST \u2013 40 jaar Eton Crop, 40 jaar DIY"))
    assert_that(event.description, equal_to("Met o.a. EC Groove Society, Quazar en Joost van Bellen"))
    assert_that(event.when, is_not(none()))
    assert_that(event.image_url, none())
    assert_that(event.date_published, is_not(none()))
    assert_that(event.source, equal_to("https://www.paradiso.nl/"))

    for event in results:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))


@pytest.mark.asyncio
async def test_sample_file_page_2(client_session: ClientSession):
    venue = ParadisoProcessor.create_venue()
    parser = ParadisoParser()
    data = await fetch(session=client_session, url=f"{venue.source_url}/page=2")

    results = parser.parse(ParsingContext(venue=venue, content=data))
    assert_that(len(results), equal_to(5))

    for event in results:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))
