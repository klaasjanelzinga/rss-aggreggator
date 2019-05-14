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
from core.parser_util import ParserUtil
from core.parsing_context import ParsingContext
from core.venue import Venue
from venues.spot.spot_config import SpotConfig


class SpotParser(Parser):
    dateformat: str = '%Y-%m-%dT:%H%M:%S%z'

    def __init__(self, config: SpotConfig):
        self.source = config.source_url
        self.base_url = config.base_url

    def parse(self, context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(context.content, 'html.parser')
        program_items = soup.find_all('article')
        return [self._transform(context.venue, f) for f in program_items]

    def _transform(self, venue: Venue, article: Tag) -> Event:
        url = article.a.get('href')
        content = article.find('div', {'class': 'program__content'})
        figure = article.find('figure').img.get('data-src')
        date = article.find('time')
        title = content.h1
        content_title = title.text if title.find('span') is None else \
            title.text.replace(title.span.text, '') + ' - ' + title.span.text
        description = ParserUtil.stripped_text_or_default_if_empty(content.p, content_title)

        return Event(url=url,
                     title=content_title,
                     description=description,
                     venue=venue,
                     image_url=f'{self.base_url}{figure}',
                     source=self.source,
                     date_published=datetime.now(),
                     when=datetime.fromisoformat(date.get('datetime')))
