import asynctest
from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that

from integration.integration_utils import with_url


class TestEndpoints(asynctest.TestCase):
    async def setUp(self) -> None:
        super().setUp()
        self.endpoint = "http://localhost:8080"
        self.session = ClientSession()
        await with_url(f"{self.endpoint}/maintenance/ping", self.session)

    async def tearDown(self) -> None:
        await self.session.close()

    async def validate(self, url: str) -> None:
        response = await self.session.get(url)
        assert_that(response.status, equal_to(200))

    async def test_events_xml(self):
        await self.validate(f"{self.endpoint}/events.xml")

    async def test_cleanup(self):
        await self.validate(f"{self.endpoint}/maintenance/cleanup")

    async def test_maintenance(self):
        await self.validate(f"{self.endpoint}/maintenance/fetch-data")
        await self.validate(f"{self.endpoint}/maintenance/ping")

    async def test_root(self):
        await self.validate(f"{self.endpoint}")

    async def test_api_events(self):
        await self.validate(f"{self.endpoint}/api/events")

    async def test_api_events_today(self):
        await self.validate(f"{self.endpoint}/api/events/today")

    async def test_api_events_tomorrow(self):
        await self.validate(f"{self.endpoint}/api/events/tomorrow")

    async def test_api_events_day_after_tomorrow(self):
        await self.validate(f"{self.endpoint}/api/events/day_after_tomorrow")

    async def test_api_venues(self):
        await self.validate(f"{self.endpoint}/api/venues")

    async def test_api_search(self):
        await self.validate(f"{self.endpoint}/api/search?term=groningen")

    async def test_channel_image(self):
        await self.validate(f"{self.endpoint}/channel-image.png")

    async def test_user_profile(self):
        response = await self.session.get(f"{self.endpoint}/api/user/profile")
        assert_that(response.status, equal_to(404))
        response = await self.session.post(
            f"{self.endpoint}/api/user/profile",
            json={"email": "klaasjanelzinga@test", "givenName": "klaasajn", "familyName": "elz"},
        )
        assert_that(response.status, equal_to(404))
        response = await self.session.post(
            f"{self.endpoint}/api/user/signup",
            json={"email": "klaasjanelzinga@test", "givenName": "klaasajn", "familyName": "elz"},
        )
        assert_that(response.status, equal_to(404))
        response = await self.session.get(
            f"{self.endpoint}/api/user/profile",
            headers={"Authorization": "Bearer 123123123123", "Accepts": "application/json"},
        )
        assert_that(response.status, equal_to(404))
        response = await self.session.get(
            f"{self.endpoint}/api/user/profile", headers={"Authorization": "Bearer", "Accepts": "application/json"}
        )
        assert_that(response.status, equal_to(404))
        response = await self.session.get(
            f"{self.endpoint}/api/user/profile", headers={"Authorization": "Beare", "Accepts": "application/json"}
        )
        assert_that(response.status, equal_to(404))
