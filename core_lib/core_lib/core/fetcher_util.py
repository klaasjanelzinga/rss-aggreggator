import locale
import threading
from contextlib import contextmanager
from typing import Generator

from aiohttp import ClientSession


async def fetch(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


LOCALE_LOCK = threading.Lock()


@contextmanager
def setlocale(name: str) -> Generator:
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)
