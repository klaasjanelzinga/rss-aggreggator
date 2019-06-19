import json
import logging
from datetime import datetime
from typing import List

import pytz
from bs4 import BeautifulSoup

from app.core.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext


class MelkwegParser(Parser):

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        venue = parsing_context.venue
        source = venue.source_url
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
                    f'scaled/agenda_thumbnail/{event["thumbnail"]}'
                url = f'https://www.melkweg.nl/nl/agenda/{event["slug"]}'
                results.append(Event(url=url,
                                     title=title,
                                     description=ParserUtil.sanitize_text(description[:1400]),
                                     venue=venue,
                                     source=source,
                                     date_published=datetime.now(),
                                     when=date,
                                     image_url=image_url
                                     ))
        logging.getLogger(__name__).info('parsed %d events melkweg', len(results))
        return results
