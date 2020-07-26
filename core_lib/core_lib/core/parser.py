import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import dateparser
import pytz
from bs4 import Tag
from dateutil.relativedelta import relativedelta

from core_lib.core.models import Event, Venue


@dataclass
class ParsingContext:
    venue: Venue
    content: str


class Parser(ABC):
    @abstractmethod
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        pass

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        pass


class ParserUtil:

    logger = logging.getLogger(__name__)

    @staticmethod
    def not_empty(text: str) -> bool:
        return text is not None and text != "" and text.strip() != ""

    @staticmethod
    def is_empty(text: str) -> bool:
        return not ParserUtil.not_empty(text)

    @staticmethod
    def has_non_empty_text(tag: Tag) -> bool:
        return tag is not None and ParserUtil.not_empty(tag.text)

    @staticmethod
    def stripped_text_or_default_if_empty(tag: Tag, default: str) -> str:
        if tag is None or ParserUtil.is_empty(tag.text):
            return default
        return tag.text.strip()

    @staticmethod
    def sanitize_text(text: str) -> str:
        return re.sub(r" {2,}", "", text).replace("\n", "")

    @staticmethod
    def remove_children_text_from(parent_tag: Tag, text: str) -> str:
        for tag in parent_tag.children:
            if isinstance(tag, Tag):
                child_text = tag.text
                text = text.replace(child_text, "")
        return text

    @staticmethod
    def parse_date_time_to_datetime(date: str, time: str, tz_str: str) -> Optional[datetime]:
        when_date = dateparser.parse(
            f"{date} {time}", languages=["nl"], settings={"TIMEZONE": tz_str, "RETURN_AS_TIMEZONE_AWARE": True}
        )
        if when_date is None:
            now = datetime.now()
            year = now.year
            when_date = dateparser.parse(
                f"{date} {year} {time}",
                languages=["nl"],
                settings={"TIMEZONE": tz_str, "RETURN_AS_TIMEZONE_AWARE": True},
            )

        if when_date is None:
            now = datetime.now()
            year = now.year + 1
            when_date = dateparser.parse(
                f"{date} {year} {time}",
                languages=["nl"],
                settings={"TIMEZONE": tz_str, "RETURN_AS_TIMEZONE_AWARE": True},
            )
        if when_date is None:
            logging.warning("Cannot parse date time from %s %s in timezone %s", date, time, tz_str)
            return None

        # If more than a year ago, we probably mean the next year.
        if when_date is not None and when_date < (datetime.now(pytz.timezone(tz_str)) - relativedelta(days=100)):
            when_date = when_date + relativedelta(years=1)
        return when_date
