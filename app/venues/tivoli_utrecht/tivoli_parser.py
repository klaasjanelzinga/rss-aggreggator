import json
from datetime import datetime
from typing import List, Dict

import dateparser  # type: ignore

from app.core.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext
from app.core.venue import Venue


class TivoliParser(Parser):

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        program_items = json.loads(parsing_context.content)
        return [TivoliParser._transform(parsing_context.venue, f) for f in program_items]

    @staticmethod
    def _transform(venue: Venue, data: Dict) -> Event:
        source = venue.source_url
        tz_short = venue.timezone_short
        url = data['link']
        title = data['title']
        image_url = data['image']
        description = data['subtitle']
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["day"]} {data["month"]} {data["year"]} 00:00{tz_short}'

        when = dateparser.parse(when_format, languages=['nl'])

        return Event(url=url,
                     title=title,
                     description=description,
                     venue=venue,
                     image_url=image_url,
                     source=source,
                     date_published=datetime.now(),
                     when=when)
