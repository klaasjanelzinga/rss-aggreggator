import json
from datetime import datetime
from typing import List, Dict

import dateparser

from app.core.event.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class ParadisoParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        program_items = json.loads(parsing_context.content)
        return [ParadisoParser._transform(parsing_context.venue, item) for item in program_items]

    @staticmethod
    def _transform(venue: Venue, data: Dict) -> Event:
        source = venue.source_url
        tz_short = venue.timezone_short
        paradiso_url = f'https://www.paradiso.nl/en/program/{data["slug"]}/{data["id"]}'
        title = data["title"]
        description = data["subtitle"]
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["start_date_time"]}{tz_short}'

        when = dateparser.parse(when_format, languages=["en"])

        return Event(
            url=paradiso_url,
            title=title,
            description=description,
            venue=venue,
            source=source,
            date_published=datetime.now(),
            when=when,
        )
