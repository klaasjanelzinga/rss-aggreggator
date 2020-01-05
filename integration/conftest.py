import asyncio
from time import sleep

from aiohttp import ClientSession, ClientTimeout
import pytest

BACKEND_URL = "http://backend:8080"


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
    url = f"{BACKEND_URL}/maintenance/cleanup-all"
    response = await session.get(url)
    if response.status > 299:
        raise Exception(f"cleanup-all failed {response}")


async def insert_default_in_datastore(session: ClientSession) -> None:
    results = [
        await session.get(f"{BACKEND_URL}/maintenance/fetch-data"),
        await session.get(f"{BACKEND_URL}/maintenance/fetch-data-1"),
    ]

    for result in results:
        if result.status > 299:
            raise Exception(f"fetch-data failed {result}")


async def init_integration_test(session: ClientSession) -> None:
    await with_url(BACKEND_URL, session)
    await clean_datastore(session)
    await insert_default_in_datastore(session)


async def call_init():
    timeout = ClientTimeout(40)
    async with ClientSession(timeout=timeout) as session:
        await asyncio.gather(init_integration_test(session))


@pytest.fixture
def backend_url() -> str:
    return BACKEND_URL


@pytest.fixture
async def client_session():
    timeout = ClientTimeout(40)
    a_client_session = ClientSession(timeout=timeout)
    yield a_client_session
    await a_client_session.close()


def pytest_runtestloop(session):
    asyncio.run(call_init())
