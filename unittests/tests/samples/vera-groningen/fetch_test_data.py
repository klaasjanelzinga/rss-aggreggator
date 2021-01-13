import asyncio

from aiohttp import ClientSession

from core_lib.core.fetcher_util import fetch
from core_lib.venues.vera_groningen import VeraSource, VeraProcessor

vera_source = VeraSource(venue=VeraProcessor.create_venue())


async def fetch_test_data():
    async with ClientSession() as session:
        file_name = "raw-fetch-{}.html"
        for page_index in range(1, 4):
            data = await fetch(url=vera_source.scrape_url.format(page_index), session=session)
            with open(file_name.format(page_index), "w") as file:
                file.write(data)


if __name__ == "__main__":
    asyncio.run(fetch_test_data())
