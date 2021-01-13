import asyncio
import os
from xml.etree import ElementTree

from aiohttp import ClientSession
from aiohttp.client import ClientTimeout


"""
1. fetch index pages from neushoorn:
curl neushoorn.nl/upcoming-events.xml

2. fetch detail pages using this script. generates the .html files in this directory and a dict for mocking.
"""


async def fetch(filename: str, client_session: ClientSession):
    directory = os.path.dirname(filename)
    with open(filename) as json_fp:
        root = ElementTree.fromstring("".join(json_fp.readlines()))
        item_no = 0
        for item in root.iter("item"):
            url = item.find("link").text
            item_no += 1
            out_filename = f"{directory}/neushoorn-{item_no}.html"
            async with client_session.get(url) as response:
                response = await response.text()
                with open(out_filename, "w") as out:
                    out.write(response)
                    print(f'      "{url}": "{out_filename}",')


async def fetch_all():
    async with ClientSession(timeout=ClientTimeout(40)) as client_session:
        await asyncio.gather(fetch("tests/samples/neushoorn-leeuwarden/upcoming-events.xml", client_session))


if __name__ == "__main__":
    asyncio.run(fetch_all())
