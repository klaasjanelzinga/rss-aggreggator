import asyncio
import os
from time import sleep

from aiohttp import ClientSession, ClientTimeout
import pytest

API_URL = "http://api:8080"
CRON_URL = "http://cron:8090"


async def with_url(url: str, session: ClientSession) -> None:
    number_of_tries = 0
    while number_of_tries < 30:
        try:
            response = await session.get(url)
            if response.status == 200:
                return
        except Exception:
            pass
        sleep(0.5)
        number_of_tries += 1


async def clean_datastore(session: ClientSession, cron_url: str) -> None:
    url = f"{cron_url}/cron/cleanup-all"
    response = await session.get(url)
    if response.status > 299:
        raise Exception(f"cleanup-all failed {response}")


async def insert_default_in_datastore(session: ClientSession, cron_url: str) -> None:
    result = await session.get(f"{cron_url}/cron/fetch-integration-test-data")
    if result.status > 299:
        raise Exception(f"fetch-data failed {result}")


async def init_integration_test(session: ClientSession, cron_url: str, api_url: str) -> None:
    await with_url(f"{cron_url}/maintenance/ping", session)
    await with_url(f"{api_url}/maintenance/ping", session)
    await clean_datastore(session, cron_url)
    await insert_default_in_datastore(session, cron_url)


async def call_init(cron_url: str, api_url: str):
    timeout = ClientTimeout(30)
    async with ClientSession(timeout=timeout) as session:
        await asyncio.gather(init_integration_test(session, cron_url, api_url))


@pytest.fixture
def event_loop():
    """
    See https://github.com/pytest-dev/pytest-asyncio/pull/156  This is required to ensure the same loop is used in
    initialization and in the test run.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def api_url() -> str:
    return os.getenv('API_URL', API_URL)


@pytest.fixture
def cron_url() -> str:
    return os.getenv('CRON_URL', CRON_URL)


@pytest.fixture
async def client_session(event_loop):
    timeout = ClientTimeout(30)
    # See https://github.com/pytest-dev/pytest-asyncio/pull/156 on why the loop is required.
    a_client_session = ClientSession(timeout=timeout, loop=event_loop)
    yield a_client_session
    await a_client_session.close()


def pytest_runtestloop(session):
    asyncio.run(call_init(api_url=os.getenv('API_URL', API_URL), cron_url=os.getenv('CRON_URL', CRON_URL)))
