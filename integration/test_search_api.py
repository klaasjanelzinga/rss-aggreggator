import base64

import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from integration.integration_utils import with_url


class TestSearchApi(asynctest.TestCase):
    async def setUp(self) -> None:
        self.endpoint = "http://localhost:8080"
        self.session = ClientSession()
        await with_url(f"{self.endpoint}/maintenance/ping", self.session)

    async def tearDown(self) -> None:
        await self.session.close()

    async def test_single_result(self):
        result = await self.session.get(
            f"{self.endpoint}/api/search", params={"term": "Beyond Hip Hop with support A Lecture By Rich Medina"}
        )
        assert_that(result.status, equal_to(200))
        json = await result.json()
        assert_that(len(json["events"]), equal_to(1))
        token: str = json["fetch_offset"]
        assert_that(base64.decodebytes(token.encode("utf-8")).decode("utf-8"), equal_to("DONE"))

    async def test_none_result(self):
        result = await self.session.get(f"{self.endpoint}/api/search", params={"term": "klaasjanelzingapython37"})
        assert_that(result.status, equal_to(200))
        json = await result.json()
        assert_that(len(json["events"]), equal_to(0))
        token: str = json["fetch_offset"]
        assert_that(base64.decodebytes(token.encode("utf-8")).decode("utf-8"), equal_to("DONE"))

    async def test_paging_result(self):
        done = False
        token = ""
        ite = 0
        tot_items = 0
        while not done:
            result = await self.session.get(
                f"{self.endpoint}/api/search", params={"term": "groningen", "fetch_offset": token}
            )
            ite += 1
            assert_that(result.status, equal_to(200))
            json = await result.json()
            tot_items += len(json["events"])
            token: str = json["fetch_offset"]
            done = base64.decodebytes(token.encode("utf-8")).decode("utf-8") == "DONE"
