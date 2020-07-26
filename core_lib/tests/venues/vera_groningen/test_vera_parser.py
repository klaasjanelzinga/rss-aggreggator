from aiohttp import ClientSession
from hamcrest import equal_to, is_not, none
from hamcrest.core import assert_that
import pytest

from core_lib.core.fetcher_util import fetch
from core_lib.core.parser import ParsingContext
from core_lib.venues.vera_groningen import VeraParser, VeraProcessor


@pytest.mark.asyncio
async def test_sample_file(client_session: ClientSession):
    venue = VeraProcessor.create_venue()
    parser = VeraParser()
    data = await fetch(session=client_session, url=f"{venue.url}/page=1")

    results = parser.parse(ParsingContext(venue=venue, content=data))
    assert_that(len(results), equal_to(20))
    event = results[0]
    assert_that(event.url, equal_to("http://www.vera-groningen.nl/?post_type=events&p=98899&lang=nl"))
    assert_that(event.venue, equal_to(venue))
    assert_that(event.title, equal_to("Beyond Hip Hop (STUDIUM GENERALE PRESENTS)"))
    assert_that(event.when, is_not(none()))
    assert_that(
        event.image_url,
        equal_to("https://www.vera-groningen.nl/content/uploads/2019/03/rich-medina-website2-360x250.jpg"),
    )
    assert_that(event.description, equal_to("Beyond Hip Hop with support A Lecture By Rich Medina"))
    assert_that(event.date_published, is_not(none()))
    assert_that(event.source, equal_to("https://www.vera-groningen.nl/programma/"))

    event = results[2]
    assert_that(event.description, equal_to("Marissa Nadler (USA) with support Klaske Oenema (NL)"))
    assert_that(event.title, equal_to("Marissa Nadler (USA)"))

    for event in results:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))


@pytest.mark.asyncio
async def test_raw_fetches(client_session: ClientSession):
    venue = VeraProcessor.create_venue()
    parser = VeraParser()
    data = await fetch(session=client_session, url=f"{venue.url}/page=1")
    results = parser.parse(ParsingContext(venue=venue, content=data))
    for event in results:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))

    data = await fetch(session=client_session, url=f"{venue.url}/page=2")
    results = parser.parse(ParsingContext(venue=venue, content=data))
    for event in results:
        assert_that(event.when, is_not(none))
        assert_that(event.description, is_not(none))
        assert_that(event.title, is_not(none))
        assert_that(event.url, is_not(none))
