import asyncio
import json
import os

from aiohttp import ClientSession
from aiohttp.client import ClientTimeout


"""
1. fetch index pages from paradiso:
https://api.paradiso.nl/api/events?lang=en&start_time=now&sort=date&order=asc&limit=30&page=1&with=locations
https://api.paradiso.nl/api/events?lang=en&start_time=now&sort=date&order=asc&limit=30&page=2&with=locations

2. fetch detail pages using this script. generates the .html files in this directory and a dict for mocking.
"""


async def fetch(filename: str, client_session: ClientSession):
    directory = os.path.dirname(filename)
    with open(filename) as json_fp:
        all_data = json.load(json_fp)
        for data in all_data:
            url = f"https://api.paradiso.nl/api/library/lists/events/{data['id']}?lang=en"
            out_filename = f"{directory}/{data['id']}.js"
            async with client_session.get(url) as response:
                response = await response.text()
                with open(out_filename, "w") as out:
                    out.write(response)
                print(f'     "{url}": "{out_filename}",')


async def fetch_all():
    async with ClientSession(timeout=ClientTimeout(40)) as client_session:
        await asyncio.gather(
            fetch("tests/samples/paradiso-amsterdam/para-1.json", client_session),
            fetch("tests/samples/paradiso-amsterdam/para-2.json", client_session),
        )


if __name__ == "__main__":
    asyncio.run(fetch_all())
