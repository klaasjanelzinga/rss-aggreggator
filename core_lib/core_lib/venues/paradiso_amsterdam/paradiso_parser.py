from datetime import datetime
import json
from typing import Dict, List

import dateparser

from core_lib.core.event.event import Event
from core_lib.core.parser import Parser
from core_lib.core.parser_util import ParserUtil
from core_lib.core.parsing_context import ParsingContext
from core_lib.core.venue.venue import Venue


class ParadisoParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        program_items = json.loads(parsing_context.content)
        return [ParadisoParser._transform(parsing_context.venue, item) for item in program_items]

    @staticmethod
    def _transform(venue: Venue, data: Dict) -> Event:
        source = venue.source_url
        paradiso_url = f'https://api.paradiso.nl/api/library/lists/events/{data["id"]}?lang=en'
        title = data["title"]
        description = data["subtitle"]
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["start_date_time"]}'

        when = dateparser.parse(
            when_format, languages=["en"], settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True}
        )

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
