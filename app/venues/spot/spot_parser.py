from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from app.core.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class SpotParser(Parser):
    dateformat: str = '%Y-%m-%dT:%H%M:%S%z'

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, 'html.parser')
        program_items = soup.find_all('article')
        return [SpotParser._transform(parsing_context.venue, f) for f in program_items]

    @staticmethod
    def _transform(venue: Venue, article: Tag) -> Event:
        source = venue.source_url
        base_url = venue.url
        url = article.a.get('href')
        content = article.find('div', {'class': 'program__content'})
        figure = article.find('figure').img.get('data-src') if article.find('figure').img else None
        date = article.find('time')
        title = content.h1
        content_title = title.text if title.find('span') is None else \
            title.text.replace(title.span.text, '') + ' - ' + title.span.text
        description = ParserUtil.stripped_text_or_default_if_empty(content.p, content_title)

        return Event(url=url,
                     title=content_title,
                     description=description,
                     venue=venue,
                     image_url=f'{base_url}{figure}',
                     source=source,
                     date_published=datetime.now(),
                     when=datetime.fromisoformat(date.get('datetime')))
