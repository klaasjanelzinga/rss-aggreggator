from datetime import datetime
from typing import List

import dateparser
from bs4 import BeautifulSoup
from bs4.element import Tag

from app.core.event import Event
from app.core.parser import Parser
from app.core.parsing_context import ParsingContext
from app.core.venue import Venue
from app.venues.oost_groningen.oost_groningen_config import OostGroningenConfig

#     <div class="agenda-item brick col m6">
#      <div class="agenda-item-inner">
#       <img alt="" class="agenda-pic" src="media/52840132_1943519875770995_7303705364178927616_o.jpg"/>
#       <span class="agenda-date">
#        13.04.2019
#                  23:59
#       </span>
#       <h3 class="sectra-light agenda-title flow-text">
#        OOST • The Clubnacht Special (attend for free entrance)
#       </h3>
#       <span class="small">DJ Leoni • Long Bram</span>
#       <div class="item-links">
#        <a class="item-link small orange" href="https://www.facebook.com/events/778633645852077/" target="_blank">
#         Meer info
#         <span class="rarr">→</span>
#        </a>
#        <a class="item-link small orange" href="https://www.facebook.com/events/778633645852077/" target="_blank">
#         Tickets
#         <span class="rarr">→</span>
#        </a>
#       </div>
#      </div>
#     </div>


class OostGroningenParser(Parser):

    def __init__(self, config: OostGroningenConfig):
        self.config = config

    def parse(self, context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(context.content, features='html.parser')
        events = soup.find_all('div', {'class': 'agenda-item'})

        return [self._transform(context.venue, tag) for tag in events]

    def _transform(self, venue: Venue, tag: Tag) -> Event:
        when_text = tag.find('span', {'class': 'agenda-date'}).text
        when_text = when_text.replace('\n', '').strip()
        when_text = when_text[0:when_text.find('/')].strip()

        when_datetime = dateparser.parse(f'{when_text}{self.config.timezone_short}', languages=['nl'])
        title = tag.find('h3', {'class': 'agenda-title'}).text
        description_tag = tag.find('span', {'class': 'small'})
        description = description_tag.text if description_tag is not None else title
        url = tag.find('a', {'class': 'item-link'}).get('href')
        image_url = f'{self.config.base_url}/{tag.find("img").get("src")}'

        return Event(url=url,
                     title=f'{title}',
                     description=description,
                     venue=venue,
                     source=self.config.base_url,
                     date_published=datetime.now(),
                     when=when_datetime,
                     image_url=image_url
                     )
