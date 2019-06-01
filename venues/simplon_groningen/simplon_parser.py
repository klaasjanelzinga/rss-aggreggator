from datetime import datetime
from typing import List

import dateparser
from bs4 import BeautifulSoup
from bs4.element import Tag

from core.event import Event
from core.parser import Parser
from core.parsing_context import ParsingContext
from core.venue import Venue
from venues.simplon_groningen.simplon_config import SimplonConfig


class SimplonParser(Parser):

    # <a data-type="concert" href="http://simplon.nl/?post_type=events&p=17412"
    # title="Idaly" class="isotope item concert">
    #     <div class="item-image" style="background-image:
    #     url(https://simplon.nl/content/uploads/2019/03/IDALY_ONTHEROAD_FINALARTWORK_CLEAN-600x600.jpg)">
    #         <div class="overlay bg-color-concert"></div>
    #                     </div>
    #     <div class="item-details">
    #         <div class="title"><h2><span>Idaly</span></h2></div>
    #         <div class="subtitle">On The Road Tour</div>        <div class="date color-concert">Za 13 April 2019</div>
    #         <div class="details">
    #             <span class="mouseover">
    #                 <br>Waar: <b>Kleine zaal</b> Open: <b>20:00 - 23:00 uur</b>
    #                 <br>VVK: <b>&euro; 11,-</b> DVK: <b>&euro; 11,-</b>                <br>
    #                 Aanvang: <b>21:00 uur</b><br>
    #             </span>
    #             Genre: <b>Hiphop / Trap</b>
    #         </div>
    #     </div>
    #     <div class="item-hitarea">
    #             <div data-ticket="https://simplon.stager.nl/web/tickets/282459" data-type="concert"
    #             class="buy-ticket color-black border-concert bg-color-concert">Koop tickets</div>
    #     </div>
    # </a>
    def __init__(self, config: SimplonConfig):
        self.config = config

    def parse(self, context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(context.content, features='html.parser')
        events = soup.find_all('a', {'class': 'item'})

        return [self._transform(context.venue, tag) for tag in events]

    def _transform(self, venue: Venue, tag: Tag) -> Event:
        url = tag.get('href')
        title = tag.get('title')
        subtitle_tag = tag.find('div', {'class': 'subtitle'})
        details_tag = tag.find('div', {'class': 'details'})
        description = subtitle_tag.text if subtitle_tag is not None else details_tag.text
        when = tag.find('div', {'class': 'date'}).text
        time = details_tag.text
        time = time[time.find('Aanvang: ') + 9: time.find('Aanvang: ') + 15]
        when_datetime = dateparser.parse(f'{when} {time}{self.config.timezone_short}')
        image_url_style = tag.find('div', {'class': 'item-image'}).get('style')
        image_url_start = image_url_style.find('https')
        image_url = image_url_style[image_url_start:image_url_style.find('.jpg') + 4]
        return Event(url=url,
                     title=f'{title}',
                     description=description,
                     venue=venue,
                     source=self.config.base_url,
                     date_published=datetime.now(),
                     when=when_datetime,
                     image_url=image_url
                     )
