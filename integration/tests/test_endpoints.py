from aiohttp import ClientSession
from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest


async def validate(client_session: ClientSession, url: str) -> None:
    response = await client_session.get(url)
    assert_that(response.status, equal_to(200))


@pytest.mark.asyncio
async def test_events_xml(client_session, api_url):
    await validate(client_session, f"{api_url}/events.xml")


@pytest.mark.asyncio
async def test_maintenance(client_session, api_url):
    await validate(client_session, f"{api_url}/maintenance/ping")


@pytest.mark.asyncio
async def test_maintenance_cron(client_session, cron_url):
    await validate(client_session, f"{cron_url}/maintenance/ping")


@pytest.mark.asyncio
async def test_api_events(client_session, api_url):
    await validate(client_session, f"{api_url}/api/events")


@pytest.mark.asyncio
async def test_api_events_today(client_session, api_url):
    await validate(client_session, f"{api_url}/api/events/today")


@pytest.mark.asyncio
async def test_api_events_tomorrow(client_session, api_url):
    await validate(client_session, f"{api_url}/api/events/tomorrow")


@pytest.mark.asyncio
async def test_api_venues(client_session, api_url):
    await validate(client_session, f"{api_url}/api/venues")


@pytest.mark.asyncio
async def test_api_search(client_session, api_url):
    await validate(client_session, f"{api_url}/api/search?term=groningen")


@pytest.mark.asyncio
async def test_user_profile(client_session, api_url):
    response = await client_session.get(f"{api_url}/api/user/profile")
    assert_that(response.status, equal_to(404))
    response = await client_session.post(
        f"{api_url}/api/user/profile",
        json={"email": "klaasjanelzinga@test", "givenName": "klaasajn", "familyName": "elz"},
    )
    assert_that(response.status, equal_to(404))
    response = await client_session.post(
        f"{api_url}/api/user/signup",
        json={"email": "klaasjanelzinga@test", "givenName": "klaasajn", "familyName": "elz"},
    )
    assert_that(response.status, equal_to(404))
    response = await client_session.get(
        f"{api_url}/api/user/profile",
        headers={"Authorization": "Bearer 123123123123", "Accepts": "application/json"},
    )
    assert_that(response.status, equal_to(404))
    response = await client_session.get(
        f"{api_url}/api/user/profile", headers={"Authorization": "Bearer", "Accepts": "application/json"}
    )
    assert_that(response.status, equal_to(404))
    response = await client_session.get(
        f"{api_url}/api/user/profile", headers={"Authorization": "Beare", "Accepts": "application/json"}
    )
    assert_that(response.status, equal_to(404))
