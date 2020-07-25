from datetime import datetime
import json
from typing import Dict, List

from bs4 import BeautifulSoup
import pytz

from core_lib.core.event.event import Event
from core_lib.core.parser import Parser
from core_lib.core.parser_util import ParserUtil
from core_lib.core.parsing_context import ParsingContext


class MelkwegParser(Parser):
    @staticmethod
    def _make_description(event: Dict) -> str:
        description_item = event["description"]
        return (
            BeautifulSoup(description_item, features="html.parser").text
            if description_item is not None
            else event["name"]
        )

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        venue = parsing_context.venue
        source = venue.source_url
        content = json.loads(parsing_context.content)

        results = []
        for day in content:
            events = [event for event in day["events"] if event["type"] == "event"]
            for event in events:
                description = MelkwegParser._make_description(event)
                date = datetime.fromtimestamp(int(event["date"]), pytz.timezone(venue.timezone))
                title = event["name"]
                image_url = (
                    f"https://s3-eu-west-1.amazonaws.com/static.melkweg.nl/uploads/images/"
                    f'scaled/agenda_thumbnail/{event["thumbnail"]}'
                )
                url = f'https://www.melkweg.nl/nl/agenda/{event["slug"]}'
                results.append(
                    Event(
                        url=url,
                        title=title,
                        description=ParserUtil.sanitize_text(description[:1400]),
                        venue=venue,
                        source=source,
                        date_published=datetime.now(),
                        when=date,
                        image_url=image_url,
                    )
                )
        return results
