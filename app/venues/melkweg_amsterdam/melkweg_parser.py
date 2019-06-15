import json
from datetime import datetime
from typing import List

import pytz
from bs4 import BeautifulSoup

from app.core.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext
from app.venues.melkweg_amsterdam.melkweg_config import MelkwegConfig


class MelkwegParser(Parser):

    def __init__(self, config: MelkwegConfig):
        self.source = config.source_url
        self.base_url = config.base_url
        self.venue_id = config.venue_id
        self.tz_short = config.timezone_short

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        venue = parsing_context.venue
        content = json.loads(parsing_context.content)

        results = []
        for day in content:
            events = [event for event in day['events'] if
                      event['type'] == 'event']
            for event in events:
                description = BeautifulSoup(event['description'], features='html.parser').text
                date = datetime.fromtimestamp(int(event['date']), pytz.timezone("Europe/Amsterdam"))
                title = event['name']
                image_url = f'https://s3-eu-west-1.amazonaws.com/static.melkweg.nl/uploads/images/' \
                    f'scaled/agenda_thumbnail/{event["id"]}'
                url = f'https://www.melkweg.nl/nl/agenda/{event["slug"]}'
                results.append(Event(url=url,
                                     title=title,
                                     description=ParserUtil.sanitize_text(description[:1400]),
                                     venue=venue,
                                     source=self.source,
                                     date_published=datetime.now(),
                                     when=date,
                                     image_url=image_url
                                     ))
        return results
