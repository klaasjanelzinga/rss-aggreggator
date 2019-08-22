from time import sleep

from aiohttp import ClientSession


async def with_url(url: str, session: ClientSession) -> None:
    number_of_tries = 0
    while number_of_tries < 30:
        try:
            response = await session.get(url)
            if response.status == 200:
                return
        except Exception:
            pass
        sleep(.5)
        number_of_tries += 1

