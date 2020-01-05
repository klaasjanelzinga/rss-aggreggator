import base64

from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest


@pytest.mark.asyncio
async def test_single_result(client_session, backend_url):
    result = await client_session.get(
        f"{backend_url}/api/search", params={"term": "Beyond Hip Hop with support A Lecture By Rich Medina"}
    )
    assert_that(result.status, equal_to(200))
    json = await result.json()
    assert_that(len(json["events"]), equal_to(1))
    token: str = json["fetch_offset"]
    assert_that(base64.decodebytes(token.encode("utf-8")).decode("utf-8"), equal_to("DONE"))

@pytest.mark.asyncio
async def test_none_result(client_session, backend_url):
    result = await client_session.get(f"{backend_url}/api/search", params={"term": "klaasjanelzingapython37"})
    assert_that(result.status, equal_to(200))
    json = await result.json()
    assert_that(len(json["events"]), equal_to(0))
    token: str = json["fetch_offset"]
    assert_that(base64.decodebytes(token.encode("utf-8")).decode("utf-8"), equal_to("DONE"))

@pytest.mark.asyncio
async def test_paging_result(client_session, backend_url):
    done = False
    token = ""
    ite = 0
    tot_items = 0
    while not done:
        result = await client_session.get(
            f"{backend_url}/api/search", params={"term": "groningen", "fetch_offset": token}
        )
        ite += 1
        assert_that(result.status, equal_to(200))
        json = await result.json()
        tot_items += len(json["events"])
        token: str = json["fetch_offset"]
        done = base64.decodebytes(token.encode("utf-8")).decode("utf-8") == "DONE"
