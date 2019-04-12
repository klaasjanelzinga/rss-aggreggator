import logging
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, Tag

#          <article class="program__item" data-datetime="1554285600"
#                  data-description="klassiek-lunchconcert-in-het-cafe-van-de-oosterpoort"
#                  data-filters="" data-genres="" data-title="lunchconcert-carlos-marin-rayo-piano">
#           <a class="program__link" href="https://www.spotgroningen.nl/programma/lunchconcert-3-april-2019/">
#            <time class="program__date" datetime="2019-04-03T12:00:00+02:00">
#              <span>wo</span><strong>3</strong><span>apr</span>
#            </time>
#            <figure class="program__figure" style="background-color: #1f1118;">
#             <img alt="" class="program__image b-lazy"
#                         data-src="/wp-content/uploads/2017/09/lunchconcerten-nieuw-150x150.jpg"
#                         src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="/>
#            </figure>
#            <div class="program__content">
#             <h1>Lunchconcert: Carlos Marín Rayo (piano)</h1>
#             <p>Klassiek lunchconcert in Het Café van De Oosterpoort</p>
#            </div>
#           </a>
#          </article>
from core.event import Event
from core.parser import Parser
from venues.spot.spot_config import SpotConfig


class SpotParser(Parser):
    dateformat: str = '%Y-%m-%dT:%H%M:%S%z'

    def __init__(self, config: SpotConfig):
        self.source = config.source_url
        self.base_url = config.base_url
        self.venue_id = config.venue_id

    def parse(self, content: str) -> List[Event]:
        soup = BeautifulSoup(content, 'html.parser')
        program_items = soup.find_all('article')
        return [self._transform(f) for f in program_items]

    @staticmethod
    def strip_optional_tag_text(tag: Tag) -> str:
        if tag is None or tag.text is None:
            return None
        return tag.text.strip()

    @staticmethod
    def is_empty(text: str) -> bool:
        return text is None or text == ''

    def _transform(self, article: Tag) -> Event:
        url = article.a.get('href')
        content = article.find('div', {'class': 'program__content'})
        figure = article.find('figure').img.get('data-src')
        date = article.find('time')
        title = content.h1
        content_title = title.text if title.find('span') is None else \
            title.text.replace(title.span.text, '') + ' - ' + title.span.text
        description_text = SpotParser.strip_optional_tag_text(content.p)
        description = description_text if not SpotParser.is_empty(description_text) else content_title

        return Event(url=url,
                     title=content_title,
                     description=description,
                     venue_id=self.venue_id,
                     image_url=f'{self.base_url}{figure}',
                     source=self.source,
                     date_published=datetime.now(),
                     when=datetime.fromisoformat(date.get('datetime')))
