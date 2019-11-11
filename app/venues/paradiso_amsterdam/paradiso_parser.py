import json
from datetime import datetime
from typing import Dict, List

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
        paradiso_url = f'https://api.paradiso.nl/api/library/lists/events/{data["id"]}?lang=en'
        title = data["title"]
        description = data["subtitle"]
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["start_date_time"]}{tz_short}'

        when = dateparser.parse(when_format, languages=["en"])

        return Event(
            url=paradiso_url,
            title=title,
            description=description,
            date_published=datetime.now(),
            venue=venue,
            source=source,
            when=when,
        )

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        additional_json = json.loads(additional_details)
        if len(additional_json) > 0:
            if "content" in additional_json[0]:
                if "alternate_urls" in additional_json[0]["content"]:
                    event.url = additional_json[0]["content"]["alternate_urls"]["en"]
                if "main_image__focus_events" in additional_json[0]["content"]:
                    main_image = additional_json[0]["content"]["main_image__focus_events"]
                    folder_path = main_image["folder_path"]
                    filename = main_image["filename"]
                    event.image_url = f"https://api.paradiso.nl/{folder_path}/{filename}"
        return event
