import json
from datetime import datetime
from typing import List, Dict

import dateparser

from core.event import Event
from core.parser import Parser
from core.parser_util import ParserUtil
# <div class="info">
# <span class="date">do 25 <em>apr</em><span class="yr"> 2019</span></span>
# <h3 class="big">Pop-O-Matic</h3>
# <h4 class="subtitle">Gratis entree – het weekend begint op donderdag!</h4> </div>
# <script type="application/ld+json">{"@context":"http:\/\/schema.org","@type":"MusicEvent","name":"Pop-O-Matic",
#   "url":"https:\/\/www.tivolivredenburg.nl\/agenda\/pop-o-matic-25-04-2019\/","startDate":"2019-04-25T23:55",
#   "location":{"@type":"LocalBusiness","name":"TivoliVredenburg","sameAs":"https:\/\/www.tivolivredenburg.nl",
#   "address":"Vredenburgkade 11, Utrecht, NL","image":""},"offers":{"@type":"offer","url":"","price":"",
#   "priceCurrency":"EUR","availability":"http:\/\/schema.org\/InStock"},
#   "image":"https:\/\/www.tivolivredenburg.nl\/wp-content\/uploads\/2019\/03\/gif-start-paars.gif"}</script></a>
# <a class="item item--agenda" href="https://www.tivolivredenburg.nl/agenda/gratis-lunchpauzeconcert-26-04-2019/"
#   data-name="gratis-lunchpauzeconcert-26-04-2019">
# <div class="image init">
# <img data-src="https://www.tivolivredenburg.nl/wp-content/uploads/2018/09/Zaal-GroteZaal-192x160.jpg"
#   src="https://www.tivolivredenburg.nl/wp-content/themes/tivolivredenburg/img/output/spacer.gif" alt=""
#   data-align="center middle" />
# </div>
from venues.tivoli_utrecht.tivoli_config import TivoliConfig


class TivoliParser(Parser):
    dateformat: str = '%Y-%m-%dT:%H%M:%S%z'

    def __init__(self, config: TivoliConfig):
        self.source = config.source_url
        self.base_url = config.base_url
        self.venue_id = config.venue_id
        self.tz_short = config.timezone_short

    def parse(self, content: str) -> List[Event]:
        program_items = json.loads(content)
        return [self._transform(f) for f in program_items]

    def _transform(self, data: Dict) -> Event:
        url = data['link']
        title = data['title']
        image_url = data['image']
        description = data['subtitle']
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["day"]} {data["month"]} {data["year"]} 00:00{self.tz_short}'

        when = dateparser.parse(when_format, languages=['nl'])

        return Event(url=url,
                     title=title,
                     description=description,
                     venue_id=self.venue_id,
                     image_url=image_url,
                     source=self.source,
                     date_published=datetime.now(),
                     when=when)
