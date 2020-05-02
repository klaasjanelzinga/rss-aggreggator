import asyncio
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


async def clean_datastore(session: ClientSession) -> None:
    url = f"{CRON_URL}/cron/cleanup-all"
    response = await session.get(url)
    if response.status > 299:
        raise Exception(f"cleanup-all failed {response}")


async def insert_default_in_datastore(session: ClientSession) -> None:
    result = await session.get(f"{CRON_URL}/cron/fetch-integration-test-data")
    if result.status > 299:
        raise Exception(f"fetch-data failed {result}")


async def init_integration_test(session: ClientSession) -> None:
    await with_url(f"{CRON_URL}/maintenance/ping", session)
    await with_url(f"{API_URL}/maintenance/ping", session)
    await clean_datastore(session)
    await insert_default_in_datastore(session)


async def call_init():
    timeout = ClientTimeout(30)
    async with ClientSession(timeout=timeout) as session:
        await asyncio.gather(init_integration_test(session))


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
    return API_URL


@pytest.fixture
def cron_url() -> str:
    return API_URL


@pytest.fixture
async def client_session(event_loop):
    timeout = ClientTimeout(30)
    # See https://github.com/pytest-dev/pytest-asyncio/pull/156 on why the loop is required.
    a_client_session = ClientSession(timeout=timeout, loop=event_loop)
    yield a_client_session
    await a_client_session.close()


def pytest_runtestloop(session):
    asyncio.run(call_init())
