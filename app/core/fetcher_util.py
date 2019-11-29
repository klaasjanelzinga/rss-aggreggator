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
    ".*paradiso.nl.*page=1.*": "tests/samples/paradiso-amsterdam/para-1.json",
    ".*paradiso.nl.*page=2.*": "tests/samples/paradiso-amsterdam/para-2.json",
    "https://api.paradiso.nl/api/library/lists/events/60445?lang=en": "tests/samples/paradiso-amsterdam/60445.js",
    "https://api.paradiso.nl/api/library/lists/events/67775?lang=en": "tests/samples/paradiso-amsterdam/67775.js",
    "https://api.paradiso.nl/api/library/lists/events/57919?lang=en": "tests/samples/paradiso-amsterdam/57919.js",
    "https://api.paradiso.nl/api/library/lists/events/63573?lang=en": "tests/samples/paradiso-amsterdam/63573.js",
    "https://api.paradiso.nl/api/library/lists/events/66875?lang=en": "tests/samples/paradiso-amsterdam/66875.js",
    "https://api.paradiso.nl/api/library/lists/events/68014?lang=en": "tests/samples/paradiso-amsterdam/68014.js",
    "https://api.paradiso.nl/api/library/lists/events/65303?lang=en": "tests/samples/paradiso-amsterdam/65303.js",
    "https://api.paradiso.nl/api/library/lists/events/61914?lang=en": "tests/samples/paradiso-amsterdam/61914.js",
    "https://api.paradiso.nl/api/library/lists/events/62928?lang=en": "tests/samples/paradiso-amsterdam/62928.js",
    "https://api.paradiso.nl/api/library/lists/events/60447?lang=en": "tests/samples/paradiso-amsterdam/60447.js",
    "https://api.paradiso.nl/api/library/lists/events/63917?lang=en": "tests/samples/paradiso-amsterdam/63917.js",
    "https://api.paradiso.nl/api/library/lists/events/58773?lang=en": "tests/samples/paradiso-amsterdam/58773.js",
    "https://api.paradiso.nl/api/library/lists/events/69558?lang=en": "tests/samples/paradiso-amsterdam/69558.js",
    "https://api.paradiso.nl/api/library/lists/events/65783?lang=en": "tests/samples/paradiso-amsterdam/65783.js",
    "https://api.paradiso.nl/api/library/lists/events/61660?lang=en": "tests/samples/paradiso-amsterdam/61660.js",
    "https://api.paradiso.nl/api/library/lists/events/67035?lang=en": "tests/samples/paradiso-amsterdam/67035.js",
    "https://api.paradiso.nl/api/library/lists/events/61766?lang=en": "tests/samples/paradiso-amsterdam/61766.js",
    "https://api.paradiso.nl/api/library/lists/events/65243?lang=en": "tests/samples/paradiso-amsterdam/65243.js",
    "https://api.paradiso.nl/api/library/lists/events/62031?lang=en": "tests/samples/paradiso-amsterdam/62031.js",
    "https://api.paradiso.nl/api/library/lists/events/65764?lang=en": "tests/samples/paradiso-amsterdam/65764.js",
    "https://api.paradiso.nl/api/library/lists/events/63196?lang=en": "tests/samples/paradiso-amsterdam/63196.js",
    "https://api.paradiso.nl/api/library/lists/events/63617?lang=en": "tests/samples/paradiso-amsterdam/63617.js",
    "https://api.paradiso.nl/api/library/lists/events/61409?lang=en": "tests/samples/paradiso-amsterdam/61409.js",
    "https://api.paradiso.nl/api/library/lists/events/65074?lang=en": "tests/samples/paradiso-amsterdam/65074.js",
    "https://api.paradiso.nl/api/library/lists/events/66064?lang=en": "tests/samples/paradiso-amsterdam/66064.js",
    "https://api.paradiso.nl/api/library/lists/events/66327?lang=en": "tests/samples/paradiso-amsterdam/66327.js",
    "https://api.paradiso.nl/api/library/lists/events/62926?lang=en": "tests/samples/paradiso-amsterdam/62926.js",
    "https://api.paradiso.nl/api/library/lists/events/67029?lang=en": "tests/samples/paradiso-amsterdam/67029.js",
    "https://api.paradiso.nl/api/library/lists/events/63182?lang=en": "tests/samples/paradiso-amsterdam/63182.js",
    "https://api.paradiso.nl/api/library/lists/events/60857?lang=en": "tests/samples/paradiso-amsterdam/60857.js",
    "https://api.paradiso.nl/api/library/lists/events/67031?lang=en": "tests/samples/paradiso-amsterdam/67031.js",
    "https://api.paradiso.nl/api/library/lists/events/63346?lang=en": "tests/samples/paradiso-amsterdam/63346.js",
    "https://api.paradiso.nl/api/library/lists/events/66347?lang=en": "tests/samples/paradiso-amsterdam/66347.js",
    "https://api.paradiso.nl/api/library/lists/events/69620?lang=en": "tests/samples/paradiso-amsterdam/69620.js",
    "https://api.paradiso.nl/api/library/lists/events/67037?lang=en": "tests/samples/paradiso-amsterdam/67037.js",
    "https://api.paradiso.nl/api/library/lists/events/62919?lang=en": "tests/samples/paradiso-amsterdam/62919.js",
    "https://api.paradiso.nl/api/library/lists/events/61411?lang=en": "tests/samples/paradiso-amsterdam/61411.js",
    "https://api.paradiso.nl/api/library/lists/events/63450?lang=en": "tests/samples/paradiso-amsterdam/63450.js",
    "https://api.paradiso.nl/api/library/lists/events/63915?lang=en": "tests/samples/paradiso-amsterdam/63915.js",
    "https://api.paradiso.nl/api/library/lists/events/65790?lang=en": "tests/samples/paradiso-amsterdam/65790.js",
    "https://api.paradiso.nl/api/library/lists/events/63032?lang=en": "tests/samples/paradiso-amsterdam/63032.js",
    "https://api.paradiso.nl/api/library/lists/events/67033?lang=en": "tests/samples/paradiso-amsterdam/67033.js",
    "https://api.paradiso.nl/api/library/lists/events/61926?lang=en": "tests/samples/paradiso-amsterdam/61926.js",
    "https://api.paradiso.nl/api/library/lists/events/59209?lang=en": "tests/samples/paradiso-amsterdam/59209.js",
    "https://api.paradiso.nl/api/library/lists/events/68105?lang=en": "tests/samples/paradiso-amsterdam/68105.js",
    "https://api.paradiso.nl/api/library/lists/events/65393?lang=en": "tests/samples/paradiso-amsterdam/65393.js",
    "https://api.paradiso.nl/api/library/lists/events/66329?lang=en": "tests/samples/paradiso-amsterdam/66329.js",
    "https://api.paradiso.nl/api/library/lists/events/62922?lang=en": "tests/samples/paradiso-amsterdam/62922.js",
    "https://api.paradiso.nl/api/library/lists/events/63834?lang=en": "tests/samples/paradiso-amsterdam/63834.js",
    "https://api.paradiso.nl/api/library/lists/events/61488?lang=en": "tests/samples/paradiso-amsterdam/61488.js",
    "https://api.paradiso.nl/api/library/lists/events/64237?lang=en": "tests/samples/paradiso-amsterdam/64237.js",
    "https://api.paradiso.nl/api/library/lists/events/65196?lang=en": "tests/samples/paradiso-amsterdam/65196.js",
    "https://api.paradiso.nl/api/library/lists/events/69156?lang=en": "tests/samples/paradiso-amsterdam/69156.js",
    "https://api.paradiso.nl/api/library/lists/events/66407?lang=en": "tests/samples/paradiso-amsterdam/66407.js",
    "https://api.paradiso.nl/api/library/lists/events/67041?lang=en": "tests/samples/paradiso-amsterdam/67041.js",
    "https://api.paradiso.nl/api/library/lists/events/61437?lang=en": "tests/samples/paradiso-amsterdam/61437.js",
    "https://api.paradiso.nl/api/library/lists/events/57161?lang=en": "tests/samples/paradiso-amsterdam/57161.js",
    "https://api.paradiso.nl/api/library/lists/events/62231?lang=en": "tests/samples/paradiso-amsterdam/62231.js",
    "https://api.paradiso.nl/api/library/lists/events/62924?lang=en": "tests/samples/paradiso-amsterdam/62924.js",
    "https://api.paradiso.nl/api/library/lists/events/58909?lang=en": "tests/samples/paradiso-amsterdam/58909.js",
    "https://www.melkweg.nl/large-json": "tests/samples/melkweg-amsterdam/-1.json",
    "https://www.melkweg.nl/.*": "tests/samples/melkweg-amsterdam/small-sample.json",
    "https://neushoorn.nl/upcoming_events": "tests/samples/neushoorn-leeuwarden/upcoming-events.xml",
    "https://neushoorn.nl/production/friejam-presenteert-the-new-conrad-miller-trio/": "tests/samples/neushoorn-leeuwarden/neushoorn-1.html",
    "https://neushoorn.nl/production/uit-de-hoge-hoed-improv-comedy-11/": "tests/samples/neushoorn-leeuwarden/neushoorn-2.html",
    "https://neushoorn.nl/production/hardcore-vrijdag-6/": "tests/samples/neushoorn-leeuwarden/neushoorn-3.html",
    "https://neushoorn.nl/production/shantel-bucovina-club-orkestar/": "tests/samples/neushoorn-leeuwarden/neushoorn-4.html",
    "https://neushoorn.nl/production/baldrs-draumar/": "tests/samples/neushoorn-leeuwarden/neushoorn-5.html",
    "https://neushoorn.nl/production/alarm-25ste-editie/": "tests/samples/neushoorn-leeuwarden/neushoorn-6.html",
    "https://neushoorn.nl/production/frou-bakker/": "tests/samples/neushoorn-leeuwarden/neushoorn-7.html",
    "https://neushoorn.nl/production/iepenup-live-maria-alyokhina-van-pussy-riot/": "tests/samples/neushoorn-leeuwarden/neushoorn-8.html",
    "https://neushoorn.nl/production/iepenup-live-23/": "tests/samples/neushoorn-leeuwarden/neushoorn-9.html",
    "https://neushoorn.nl/production/matt-bianco/": "tests/samples/neushoorn-leeuwarden/neushoorn-10.html",
    "https://neushoorn.nl/production/psyfreaks-3/": "tests/samples/neushoorn-leeuwarden/neushoorn-11.html",
    "https://neushoorn.nl/production/levi-weemoedt/": "tests/samples/neushoorn-leeuwarden/neushoorn-12.html",
    "https://neushoorn.nl/production/julia-zahra/": "tests/samples/neushoorn-leeuwarden/neushoorn-13.html",
    "https://neushoorn.nl/production/lcls-invites-sputnik/": "tests/samples/neushoorn-leeuwarden/neushoorn-14.html",
    "https://neushoorn.nl/production/a-special-holiday-event-with-arstidir/": "tests/samples/neushoorn-leeuwarden/neushoorn-15.html",
    "https://neushoorn.nl/production/insomnium-the-black-dahlia-murder-stam1na/": "tests/samples/neushoorn-leeuwarden/neushoorn-16.html",
    "https://neushoorn.nl/production/downtown-cafe-tromptheater/": "tests/samples/neushoorn-leeuwarden/neushoorn-17.html",
    "https://www.hedon-zwolle.nl/#programma": "tests/samples/hedon-zwolle/programma.html",
    "https://www.013.nl/programma": "tests/samples/t013-tilburg/programma.html",
}


async def fetch(session: ClientSession, url: str) -> str:
    if AppConfig.is_running_in_gae():
        async with session.get(url) as response:
            return await response.text()
    logging.getLogger(__name__).warning("Retrieving stubbed data locally for %s", url)
    filename = URL_TO_MOCK_FILE_DICT.get(url)
    if filename is None:
        for key, value in URL_TO_MOCK_FILE_DICT.items():
            if re.match(key, url):
                filename = value
                break
    if filename is None:
        raise Exception(f"No support for stubbed url {url}")
    async with aiofiles.open(filename) as file:
        lines = await file.readlines()

        def fix_a_line(line: str) -> str:
            result = line
            match = re.search(r"{{random_future_date:(.*?)}}", result)
            while match:
                result = fix(result)
                match = re.search(r"{{random_future_date:(.*?)}}", result)
            return result

        fixed_lines = [fix_a_line(line) for line in lines]
        return "".join(fixed_lines)
