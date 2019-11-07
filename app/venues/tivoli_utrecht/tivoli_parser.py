import json
from datetime import datetime
from typing import Dict, List

import dateparser
from bs4 import BeautifulSoup

from app.core.event.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class TivoliParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        program_items = json.loads(parsing_context.content)
        return [TivoliParser._transform(parsing_context.venue, f) for f in program_items]

    @staticmethod
    def _transform(venue: Venue, data: Dict) -> Event:
        source = venue.source_url
        tz_short = venue.timezone_short
        tivoli_url = data["link"]
        title = data["title"]
        image_url = data["image"]
        description = data["subtitle"]
        description = description if ParserUtil.not_empty(description) else title
        when_format = f'{data["day"]} {data["month"]} {data["year"]} 00:00{tz_short}'

        when = dateparser.parse(when_format, languages=["nl"])

        return Event(
            url=tivoli_url,
            title=title,
            description=description,
            venue=venue,
            image_url=image_url,
            source=source,
            date_published=datetime.now(),
            when=when,
        )

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        soup = BeautifulSoup(additional_details, features="html.parser")
        # find a div with info-inner/label containing a span "aanvang"
        time = None
        for div in soup.find_all("div", {"class": "info-inner"}):
            label = div.find("div", {"class": "label"})
            if label and label.find("span").text == "aanvang":
                time = div.find("div", {"class": "values"}).find("span").text
        if time and len(time.split(":")) == 2:
            event.when = event.when.replace(hour=int(time.split(":")[0]), minute=int(time.split(":")[1]))
        return event
