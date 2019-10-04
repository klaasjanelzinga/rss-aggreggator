import logging
import re

import aiofiles
from aiohttp import ClientSession

from app.core.app_config import AppConfig
from app.core.data_fixer import fix

URL_TO_MOCK_FILE_DICT = {
    ".*spotgroningen.*": "tests/samples/spot/Programma - Spot Groningen.html",
    ".*vera-groningen.*page=1.*": "tests/samples/vera-groningen/raw-fetch-0.html",
    ".*vera-groningen.*page=2.*": "tests/samples/vera-groningen/raw-fetch-1.html",
    ".*simplon.nl.*": "tests/samples/simplon-groningen/Simplon.html",
    ".*komoost.nl.*": "tests/samples/oost-groningen/komoost.html",
    ".*tivolivredenburg.nl.*page=1.*": "tests/samples/tivoli-utrecht/ajax-1.js",
    ".*tivolivredenburg.nl.*page=2.*": "tests/samples/tivoli-utrecht/ajax-2.js",
    ".*paradiso.nl.*page=1.*": "tests/samples/paradiso-amsterdam/ajax-1.js",
    ".*paradiso.nl.*page=2.*": "tests/samples/paradiso-amsterdam/ajax-2.js",
    "https://www.melkweg.nl/large-json": "tests/samples/melkweg-amsterdam/-1.json",
    "https://www.melkweg.nl/.*": "tests/samples/melkweg-amsterdam/small-sample.json",
}


async def fetch(session: ClientSession, url: str) -> str:
    if AppConfig.is_running_in_gae():
        async with session.get(url) as response:
            return await response.text()
    logging.getLogger(__name__).warning("Retrieving stubbed data locally for %s", url)
    for key, value in URL_TO_MOCK_FILE_DICT.items():
        if re.match(key, url):
            async with aiofiles.open(value) as file:
                lines = await file.readlines()
                fixed_lines = [fix(line) for line in lines]
                return "".join(fixed_lines)
    raise Exception(f"No support for stubbed url {url}")
