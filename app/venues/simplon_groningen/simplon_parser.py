from datetime import datetime
from typing import List

import dateparser
from bs4 import BeautifulSoup
from bs4.element import Tag

from app.core.event.event import Event
from app.core.parser import Parser
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class SimplonParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, features="html.parser")
        events = soup.find_all("a", {"class": "item"})

        return [SimplonParser._transform(parsing_context.venue, tag) for tag in events]

    @staticmethod
    def _transform(venue: Venue, tag: Tag) -> Event:
        simplon_url = tag.get("href")
        title = tag.get("title")
        subtitle_tag = tag.find("div", {"class": "subtitle"})
        details_tag = tag.find("div", {"class": "details"})
        description = subtitle_tag.text if subtitle_tag is not None else details_tag.text
        when = tag.find("div", {"class": "date"}).text
        time = details_tag.text
        time = time[time.find("Aanvang: ") + 9 : time.find("Aanvang: ") + 15]

        when_datetime = dateparser.parse(
            f"{when} {time}", settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True}
        )
        image_url_style = tag.find("div", {"class": "item-image"}).get("style")
        image_url_start = image_url_style.find("https")
        image_url = image_url_style[image_url_start : image_url_style.find(".jpg") + 4]
        return Event(
            url=simplon_url,
            title=f"{title}",
            description=description,
            venue=venue,
            source=venue.url,
            date_published=datetime.now(),
            when=when_datetime,
            image_url=image_url,
        )
