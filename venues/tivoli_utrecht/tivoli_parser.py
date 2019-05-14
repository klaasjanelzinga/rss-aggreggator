import json
from datetime import datetime
from typing import List, Dict

import dateparser

from core.event import Event
from core.parser import Parser
from core.parser_util import ParserUtil
from core.parsing_context import ParsingContext
from core.venue import Venue
from venues.tivoli_utrecht.tivoli_config import TivoliConfig


class TivoliParser(Parser):

    def __init__(self, config: TivoliConfig):
        self.source = config.source_url
        self.base_url = config.base_url
        self.venue_id = config.venue_id
        self.tz_short = config.timezone_short

    def parse(self, context: ParsingContext) -> List[Event]:
        program_items = json.loads(context.content)
        return [self._transform(context.venue, f) for f in program_items]

    def _transform(self, venue: Venue, data: Dict) -> Event:
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
                     venue=venue,
                     image_url=image_url,
                     source=self.source,
                     date_published=datetime.now(),
                     when=when)
