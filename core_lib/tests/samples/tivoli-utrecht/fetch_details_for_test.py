import asyncio
import json
import os

from aiohttp import ClientSession
from aiohttp.client import ClientTimeout


"""
1. fetch index pages from tivoli:
curl 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page=2&categorie=&maand=' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://www.tivolivredenburg.nl/agenda/' -H 'Cookie: __cfduid=d35c04a000a582a13b13493a2ece5fc0a1570183558; cookie_settings=default; _ga=GA1.2.4955337.1570380863; _hjid=6c0b453e-233b-4f40-85fe-96742de77186; _gid=GA1.2.157363698.1572892830; _gat_UA-46364837-1=1; _gali=agenda-overview' -H 'TE: Trailers' > ajax-2.js
curl 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page=1&categorie=&maand=' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://www.tivolivredenburg.nl/agenda/' -H 'Cookie: __cfduid=d35c04a000a582a13b13493a2ece5fc0a1570183558; cookie_settings=default; _ga=GA1.2.4955337.1570380863; _hjid=6c0b453e-233b-4f40-85fe-96742de77186; _gid=GA1.2.157363698.1572892830; _gat_UA-46364837-1=1; _gali=agenda-overview' -H 'TE: Trailers' > ajax-1.js

2. fetch detail pages using this script. generates the .html files in this directory and a dict for mocking.
"""


async def fetch(filename: str, client_session: ClientSession):
    directory = os.path.dirname(filename)
    with open(filename) as json_fp:
        data = json.load(json_fp)
        for i in data:
            url = i["link"]
            url_parts = url.split("/")
            out_filename = f"{directory}/{url_parts[-2]}.html"
            async with client_session.get(url) as response:
                response = await response.text()
                with open(out_filename, "w") as out:
                    out.write(response)
                print(f'     "{url}": "{out_filename}",')


async def fetch_all():
    async with ClientSession(timeout=ClientTimeout(40)) as client_session:
        await asyncio.gather(
            fetch("tests/samples/tivoli-utrecht/ajax-1.json", client_session),
            fetch("tests/samples/tivoli-utrecht/ajax-2.json", client_session),
        )


if __name__ == "__main__":
    asyncio.run(fetch_all())
