from datetime import datetime
from typing import List
from xml.etree import ElementTree

from bs4 import BeautifulSoup

from app.core.event.event import Event
from app.core.parser import Parser
from app.core.parser_util import ParserUtil
from app.core.parsing_context import ParsingContext


class NeushoornParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        root = ElementTree.fromstring(parsing_context.content)
        events = []
        for item in root.iter("item"):
            maybe_url = item.find("link")
            maybe_description = item.find("description")
            maybe_title = item.find("title")
            if maybe_url is None or maybe_title is None or maybe_description is None:
                break
            url = maybe_url.text
            description = maybe_description.text
            title = maybe_title.text
            events.append(
                Event(
                    url=str(url),
                    title=str(title),
                    description=str(description),
                    venue=parsing_context.venue,
                    source=parsing_context.venue.url,
                    date_published=datetime.now(),
                    when=datetime.min,
                    image_url=None,
                )
            )
        return events

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        soup = BeautifulSoup(additional_details, features="html.parser")
        image_url = None
        when_date = None
        if soup.find("meta", {"name": "twitter:image"}) is not None:
            image_url = soup.find("meta", {"name": "twitter:image"})["content"]
        if soup.find("meta", {"property": "og:image"}):
            image_url = soup.find("meta", {"property": "og:image"})["content"]
        summary_div = soup.find("div", {"class": "summary"})
        summary_item_divs = summary_div.find_all("div", {"class": "summary__item"})
        if len(summary_item_divs) == 2:
            date = summary_item_divs[0].text
            time = summary_item_divs[1].text
            date = ParserUtil.sanitize_text(date)
            time = ParserUtil.sanitize_text(time)
            time = time[time.index("Aanvang ") + 8 :]
            when_date = ParserUtil.parse_date_time_to_datetime(date, time, event.venue.timezone)

        if when_date is not None:
            event.when = when_date
        event.image_url = image_url
        return event
