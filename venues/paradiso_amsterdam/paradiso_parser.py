import json
from datetime import datetime
from typing import List, Dict

import dateparser

from core.event import Event
from core.parser import Parser
from core.parser_util import ParserUtil
from venues.paradiso_amsterdam.paradiso_config import ParadisoConfig


class ParadisoParser(Parser):

    def __init__(self, config: ParadisoConfig):
        self.source = config.source_url
        self.base_url = config.base_url
        self.venue_id = config.venue_id
        self.tz_short = config.timezone_short

    def parse(self, content: str) -> List[Event]:
        program_items = json.loads(content)
        return [self._transform(f) for f in program_items]

    def _transform(self, data: Dict) -> Event:
        url = f'https://www.paradiso.nl/en/program/{data["slug"]}/{data["id"]}'
        title = data['title']
        description = data['subtitle']
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["start_date_time"]}{self.tz_short}'

        when = dateparser.parse(when_format, languages=['en'])

        return Event(url=url,
                     title=title,
                     description=description,
                     venue_id=self.venue_id,
                     source=self.source,
                     date_published=datetime.now(),
                     when=when)
