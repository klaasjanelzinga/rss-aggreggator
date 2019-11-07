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
    ".*tivolivredenburg.nl.*page=1.*": "tests/samples/tivoli-utrecht/ajax-1",
    ".*tivolivredenburg.nl.*page=2.*": "tests/samples/tivoli-utrecht/ajax-2",
    "https://www.tivolivredenburg.nl/agenda/schumann-quartett-04-11-2019/": "tests/samples/tivoli-utrecht/schumann-quartett-04-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/ilfu-book-talk-met-jeanette-winterson-04-11-2019/": "tests/samples/tivoli-utrecht/ilfu-book-talk-met-jeanette-winterson-04-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/ryan-mcmullan-13-11-2019/": "tests/samples/tivoli-utrecht/ryan-mcmullan-13-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/wat-een-ramp-3-rouw-en-veerkracht-04-11-2019/": "tests/samples/tivoli-utrecht/wat-een-ramp-3-rouw-en-veerkracht-04-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/rabo-open-stage-the-intimate-sessions-13-11-2019/": "tests/samples/tivoli-utrecht/rabo-open-stage-the-intimate-sessions-13-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/herbie-hancock-04-11-2019/": "tests/samples/tivoli-utrecht/herbie-hancock-04-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/matthew-and-the-atlas-13-11-2019/": "tests/samples/tivoli-utrecht/matthew-and-the-atlas-13-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/opeth-05-11-2019/": "tests/samples/tivoli-utrecht/opeth-05-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/alice-phoebe-lou-13-11-2019/": "tests/samples/tivoli-utrecht/alice-phoebe-lou-13-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/calexico-and-iron-wine-05-11-2019/": "tests/samples/tivoli-utrecht/calexico-and-iron-wine-05-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/duncan-laurence-13-11-2019/": "tests/samples/tivoli-utrecht/duncan-laurence-13-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/charles-lloyd-quintet-05-11-2019/": "tests/samples/tivoli-utrecht/charles-lloyd-quintet-05-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/ilfu-book-talk-met-louis-theroux-14-11-2019/": "tests/samples/tivoli-utrecht/ilfu-book-talk-met-louis-theroux-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/bye-bye-britain-05-11-2019/": "tests/samples/tivoli-utrecht/bye-bye-britain-05-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/the-specials-14-11-2019/": "tests/samples/tivoli-utrecht/the-specials-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/of-monsters-and-men-06-11-2019/": "tests/samples/tivoli-utrecht/of-monsters-and-men-06-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/the-mountain-goats-14-11-2019/": "tests/samples/tivoli-utrecht/the-mountain-goats-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/transforming-stories-06-11-2019/": "tests/samples/tivoli-utrecht/transforming-stories-06-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/electric-six-14-11-2019/": "tests/samples/tivoli-utrecht/electric-six-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/future-sounds-nederlandse-pop-academie-on-stage-06-11-2019/": "tests/samples/tivoli-utrecht/future-sounds-nederlandse-pop-academie-on-stage-06-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/heilung-14-11-2019/": "tests/samples/tivoli-utrecht/heilung-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/christian-scott-atunde-adjuah-06-11-2019/": "tests/samples/tivoli-utrecht/christian-scott-atunde-adjuah-06-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/luka-bloom-14-11-2019/": "tests/samples/tivoli-utrecht/luka-bloom-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/le-guess-who-2019-donderdag-07-11-2019/": "tests/samples/tivoli-utrecht/le-guess-who-2019-donderdag-07-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/perforator-14-11-2019/": "tests/samples/tivoli-utrecht/perforator-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/le-guess-who-2019-passe-partout-07-11-2019/": "tests/samples/tivoli-utrecht/le-guess-who-2019-passe-partout-07-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/zuco-103-14-11-2019/": "tests/samples/tivoli-utrecht/zuco-103-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/pop-o-matic-14-11-2019/": "tests/samples/tivoli-utrecht/pop-o-matic-14-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/pop-o-matic-07-11-2019/": "tests/samples/tivoli-utrecht/pop-o-matic-07-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/gratis-lunchpauzeconcert-15-11-2019/": "tests/samples/tivoli-utrecht/gratis-lunchpauzeconcert-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/le-guess-who-2019-vrijdag-08-11-2019/": "tests/samples/tivoli-utrecht/le-guess-who-2019-vrijdag-08-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/avrotros-vrijdagconcert-08-11-2019/": "tests/samples/tivoli-utrecht/avrotros-vrijdagconcert-08-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/job-roggeveen-x-pieces-of-tomorrow-festival-keys-of-light-15-11-2019/": "tests/samples/tivoli-utrecht/job-roggeveen-x-pieces-of-tomorrow-festival-keys-of-light-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/park-6-by-night-gesloten-08-11-2019/": "tests/samples/tivoli-utrecht/park-6-by-night-gesloten-08-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/kensington-15-11-2019/": "tests/samples/tivoli-utrecht/kensington-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/le-guess-who-2019-zaterdag-09-11-2019/": "tests/samples/tivoli-utrecht/le-guess-who-2019-zaterdag-09-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/park-6-by-night-gesloten-09-11-2019/": "tests/samples/tivoli-utrecht/park-6-by-night-gesloten-09-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/avrotros-vrijdagconcert-15-11-2019/": "tests/samples/tivoli-utrecht/avrotros-vrijdagconcert-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/le-guess-who-2019-zondag-10-11-2019/": "tests/samples/tivoli-utrecht/le-guess-who-2019-zondag-10-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/the-chats-15-11-2019/": "tests/samples/tivoli-utrecht/the-chats-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/3fm-serious-request-gametoernooi-11-11-2019/": "tests/samples/tivoli-utrecht/3fm-serious-request-gametoernooi-11-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/cass-mccombs-15-11-2019/": "tests/samples/tivoli-utrecht/cass-mccombs-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/ibrahim-maalouf-11-11-2019/": "tests/samples/tivoli-utrecht/ibrahim-maalouf-11-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/taksim-trio-15-11-2019/": "tests/samples/tivoli-utrecht/taksim-trio-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/andy-mckee-11-11-2019/": "tests/samples/tivoli-utrecht/andy-mckee-11-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/a-song-journey-15-11-2019/": "tests/samples/tivoli-utrecht/a-song-journey-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/worry-dolls-11-11-2019/": "tests/samples/tivoli-utrecht/worry-dolls-11-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/park-6-by-night-15-11-2019/": "tests/samples/tivoli-utrecht/park-6-by-night-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/bruce-hornsby-11-11-2019/": "tests/samples/tivoli-utrecht/bruce-hornsby-11-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/kombucha-workshop-in-park-6-15-11-2019/": "tests/samples/tivoli-utrecht/kombucha-workshop-in-park-6-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/het-nieuwe-ouderschap-12-11-2019/": "tests/samples/tivoli-utrecht/het-nieuwe-ouderschap-12-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/rabo-open-stage-djangus-15-11-2019/": "tests/samples/tivoli-utrecht/rabo-open-stage-djangus-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/amsterdam-sinfonietta-12-11-2019/": "tests/samples/tivoli-utrecht/amsterdam-sinfonietta-12-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/gitaardisco-15-11-2019/": "tests/samples/tivoli-utrecht/gitaardisco-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/b-boys-12-11-2019/": "tests/samples/tivoli-utrecht/b-boys-12-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/mad-izm-15-11-2019/": "tests/samples/tivoli-utrecht/mad-izm-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/zin-in-muziek-2-12-11-2019/": "tests/samples/tivoli-utrecht/zin-in-muziek-2-12-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/blackout-15-11-2019/": "tests/samples/tivoli-utrecht/blackout-15-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/pieces-of-tomorrow-festival-16-11-2019/": "tests/samples/tivoli-utrecht/pieces-of-tomorrow-festival-16-11-2019.html",
    "https://www.tivolivredenburg.nl/agenda/park-6-by-night-gesloten-16-11-2019/": "tests/samples/tivoli-utrecht/park-6-by-night-gesloten-16-11-2019.html",
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
