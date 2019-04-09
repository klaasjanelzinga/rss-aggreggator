import logging
import re
from datetime import datetime
from typing import List

import dateparser
from bs4 import BeautifulSoup, Tag

from core.event import Event
from core.parser import Parser
from venues.vera_groningen.vera_config import VeraConfig


# parsing
# <div class="col-xs-60 col-lg-60 event-wrapper fade-in nopad-hor">
#  <div class="row nopad-vert">
#   <a class="event-link vert-aligneable-container extra-event" href="http://www.vera-groningen.nl/?post_type=events&amp;p=99134&amp;lang=nl">
#    <div class="fade-in col-sm-18 col-md-13 col-lg-11 nopad hidden-xs-down">
#     <div class="image artist-image" style="background-image: url('https://www.vera-groningen.nl/content/uploads/2019/03/Sirene-Bouke-Groen-1-2-360x250.jpg');">
#     </div>
#    </div>
#    <div class="col-xs-60 col-sm-34 col-md-39 col-lg-41 nopad-vert pull-down data">
#     <div class="date">zondag  7 april</div>
#     <h3 class="artist">CLASH XXL Expo<sup class="origin"></sup></h3>
#     <div>
#      <h4 class="extra">Bouke Groen: Sirene<sup class="origin">
#          </sup>+ Lilnu' me Veen: SCHLÆGERCORE<sup class="origin"></sup>
#     </h4>
#     </div>
#     <div class="schedule">Extra | Ticket: Gratis | doors: 14:00 - 18:00 | start: 14:00</div>
#    </div>
#    <div class="col-xs-60 col-sm-8 col-md-8 col-lg-8 nopad pull-down visible-sm-up">
#     <object><a class="button hvr-shutter-out-vertical extra-event free-event" href="http://www.vera-groningen.nl/?post_type=events&amp;p=99134&amp;lang=nl" target="_blank">Gratis</a></object>
#    </div>
#   </a>
#  </div>
# </div>
class VeraParser(Parser):

    def __init__(self, config: VeraConfig):
        self.source = config.source
        self.base_url = config.base_url
        self.venue_id = config.venue_id

    def parse(self, content: str) -> List[Event]:
        soup = BeautifulSoup(content, features='html.parser')
        events = soup.find_all('div', {'class': 'event-wrapper'})

        logging.info(f'found {len(events)} event in {self.source}')
        return [self._transform(tag) for tag in events]

    @staticmethod
    def _sanitize_text(text: str) -> str:
        return re.sub(r'[\ \ ]{2,}', '', text).replace('\n', '')

    @staticmethod
    def _remove_children_text_from(parent_tag: Tag, text: str) -> str:
        for tag in parent_tag.children:
            if isinstance(tag, Tag):
                child_text = tag.text
                text = text.replace(child_text, '')
        return text

    @staticmethod
    def _add_sup_text_from_text(parent_tag: Tag, text: str) -> str:
        sup = parent_tag.find('sup')
        if sup is None or len(sup.text.strip()) == 0:
            return text
        return f'{text} ({sup.text})'

    def _transform(self, tag: Tag) -> Event:
        url = tag.find('a', {'class': 'event-link'})['href']
        artist_tag = tag.find('h3', {'class': re.compile(r'artist|artist ')})
        if artist_tag is not None:
            artist = VeraParser._remove_children_text_from(artist_tag, artist_tag.text)
            artist = VeraParser._add_sup_text_from_text(artist_tag, artist)
            artist = VeraParser._sanitize_text(artist)
        else:
            artist = url

        extra_tag = tag.find('h4', {'class': 'extra'})
        if extra_tag is not None:
            extra = VeraParser._remove_children_text_from(extra_tag, extra_tag.text)
            extra = VeraParser._add_sup_text_from_text(extra_tag, extra)
            extra = VeraParser._sanitize_text(extra)
        else:
            extra = ''

        extra_title = tag.find('h4', {'class': 'pretitle'})
        if extra_title is not None:
            extra_title = f'({VeraParser._sanitize_text(extra_title.text)})'
        else:
            extra_title = ''

        when_tag = tag.find('div', {'class': 'date'})
        if when_tag is not None:
            when = VeraParser._remove_children_text_from(when_tag, when_tag.text)
            when = VeraParser._sanitize_text(when)
            when_time = tag.find('div', {'class': 'schedule'}).text
            when_time = when_time[when_time.find('start: ') + 7:when_time.find('start: ') + 12]
            when_date: datetime = dateparser.parse(f'{when} {when_time}+02:00', languages=['nl'])
        else:
            when_date = datetime.min
        image_url = tag.find('div', {'class': 'artist-image'})['style']
        image_url_end = image_url.find('\'', image_url.find('https') + 4)
        image_url = image_url[image_url.find('https'):image_url_end]

        return Event(url=url,
                     title=f'{artist} {extra_title}'.strip(),
                     description=f'{artist}{" with support" if extra != "" else ""} {extra}'.strip(),
                     venue_id=self.venue_id,
                     source=self.source,
                     date_published=datetime.now(),
                     when=when_date,
                     image_url=image_url)
