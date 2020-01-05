import base64

from hamcrest import equal_to, is_not
from hamcrest.core import assert_that
import pytest


@pytest.mark.asyncio
async def test_first_fetch(client_session, backend_url):
    result = await client_session.get(f"{backend_url}/api/events", params={"fetch_offset": ""})
    assert_that(result.status, equal_to(200))
    json = await result.json()
    assert_that(len(json["events"]), equal_to(25))
    token: str = json["fetch_offset"]
    assert_that(base64.decodebytes(token.encode("utf-8")).decode("utf-8"), is_not(equal_to("DONE")))

@pytest.mark.asyncio
async def test_paging(client_session, backend_url):
    result = await client_session.get(f"{backend_url}/api/events", params={"fetch_offset": ""})
    assert_that(result.status, equal_to(200))
    json = await result.json()
    assert_that(len(json["events"]), equal_to(25))
    first_event_id = json["events"][0]["id"]
    token: str = json["fetch_offset"]
    result = await client_session.get(f"{backend_url}/api/events", params={"fetch_offset": token})
    assert_that(result.status, equal_to(200))
    json = await result.json()
    assert_that(len(json["events"]), equal_to(25))
    second_event_id = json["events"][0]["id"]
    assert_that(first_event_id, is_not(equal_to(second_event_id)))
