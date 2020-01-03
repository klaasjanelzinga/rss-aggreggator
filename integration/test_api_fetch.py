import base64

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from integration.integration_utils import BACKEND_URL, with_url


class TestApiFetch(asynctest.TestCase):
    async def setUp(self) -> None:
        self.endpoint = BACKEND_URL
        self.session = ClientSession()
        await with_url(f"{self.endpoint}/maintenance/ping", self.session)

    async def tearDown(self) -> None:
        await self.session.close()

    async def test_first_fetch(self):
        result = await self.session.get(f"{self.endpoint}/api/events", params={"fetch_offset": ""})
        assert_that(result.status, equal_to(200))
        json = await result.json()
        assert_that(len(json["events"]), equal_to(25))
        token: str = json["fetch_offset"]
        assert_that(base64.decodebytes(token.encode("utf-8")).decode("utf-8"), is_not(equal_to("DONE")))

    async def test_paging(self):
        result = await self.session.get(f"{self.endpoint}/api/events", params={"fetch_offset": ""})
        assert_that(result.status, equal_to(200))
        json = await result.json()
        assert_that(len(json["events"]), equal_to(25))
        first_event_id = json["events"][0]["id"]
        token: str = json["fetch_offset"]
        result = await self.session.get(f"{self.endpoint}/api/events", params={"fetch_offset": token})
        assert_that(result.status, equal_to(200))
        json = await result.json()
        assert_that(len(json["events"]), equal_to(25))
        second_event_id = json["events"][0]["id"]
        assert_that(first_event_id, is_not(equal_to(second_event_id)))
