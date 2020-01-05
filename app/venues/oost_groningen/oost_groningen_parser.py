from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag
import dateparser

from app.core.event.event import Event
from app.core.parser import Parser
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class OostGroningenParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, features="html.parser")
        events = soup.find_all("div", {"class": "agenda-item"})

        return [OostGroningenParser._transform(parsing_context.venue, tag) for tag in events]

    @staticmethod
    def _transform(venue: Venue, tag: Tag) -> Event:
        when_text = tag.find("span", {"class": "agenda-date"}).text
        when_text = when_text.replace("\n", "").strip()
        when_text = when_text[0 : when_text.find("/")].strip()

        when_datetime = dateparser.parse(
            f"{when_text}", languages=["nl"], settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True},
        )
        title = tag.find("h3", {"class": "agenda-title"}).text
        description_tag = tag.find("span", {"class": "small"})
        description = description_tag.text if description_tag is not None else title
        oost_url = tag.find("a", {"class": "item-link"}).get("href")
        image_url = f'{venue.url}/{tag.find("img").get("src")}'

        return Event(
            url=oost_url,
            title=f"{title}",
            description=description,
            venue=venue,
            source=venue.source_url,
            date_published=datetime.now(),
            when=when_datetime,
            image_url=image_url,
        )
