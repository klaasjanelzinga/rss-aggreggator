import base64
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Any

import pytz


def split_term(term: str) -> List[str]:
    return [re.sub(r"[^\w]+", "", t.lower()) for t in re.split(" |-", term) if len(t) > 3]


@dataclass
class Venue:
    name: str
    short_name: str
    url: str
    venue_id: str
    email: str
    phone: str
    city: str
    country: str
    timezone: str
    source_url: str
    last_fetched_date: datetime = datetime(1900, 1, 1, 1, 1, 1, 0, pytz.utc)
    search_terms: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.search_terms = [term.lower() for term in split_term(self.name) + [self.city]]

    def convert_utc_to_venue_timezone(self, when: datetime) -> datetime:
        venue_tz = pytz.timezone(self.timezone)
        return when.astimezone(venue_tz)


@dataclass
class Event:
    url: str
    title: str
    description: str
    venue: Venue
    source: str
    date_published: datetime
    when: Optional[datetime]
    image_url: Optional[str] = None
    search_terms: List[str] = field(default_factory=list)
    event_id: str = field(default_factory=str)

    def __post_init__(self) -> None:
        self.event_id = str(base64.encodebytes(bytes(self.url, "utf-8")), "utf-8") if self.url is not None else None
        self.search_terms = self.generate_search_terms()

    def __eq__(self, other: Any) -> bool:
        return self.event_id == other.event_id

    def __hash__(self) -> int:
        return hash(self.event_id)

    def update_url(self, new_url: str) -> None:
        """ Updates event_id as well! Use at own risk. """
        self.url = new_url
        self.event_id = str(base64.encodebytes(bytes(self.url, "utf-8")), "utf-8") if self.url is not None else None

    def generate_search_terms(self) -> List[str]:
        search_terms = split_term(self.title) + split_term(self.description)
        search_terms = [re.sub(r"[^\w]+", "", term.lower()) for term in search_terms if len(term) > 3]
        search_terms.extend(self.venue.search_terms)
        return [term for term in search_terms if len(term) > 3]

    def __repr__(self) -> str:
        return f"core.Event {self.url} {self.title} {self.description}"

    @staticmethod
    def is_not_empty(text: str) -> bool:
        return text is not None and text != ""

    def is_valid(self) -> bool:
        valid_date = self.when is not None and self.when > datetime.now(pytz.timezone(self.venue.timezone))
        valid = (
            Event.is_not_empty(self.title)
            and Event.is_not_empty(self.description)
            and valid_date
            and Event.is_not_empty(self.url)
        )
        if not valid:
            logging.getLogger(__name__).warning("Invalid event %s", self)
        return valid
