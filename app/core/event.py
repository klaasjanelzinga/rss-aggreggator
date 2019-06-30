import base64
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Any

import pytz

from app.core.datastore_utils import DatastoreUtils
from app.core.venue import Venue


@dataclass
class Event:
    url: str
    title: str
    description: str
    venue: Venue
    source: str
    date_published: datetime
    when: datetime
    image_url: Optional[str] = None
    search_terms: Optional[List[str]] = None
    event_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.event_id = str(base64.encodebytes(bytes(self.url, 'utf-8')), 'utf-8') if self.url is not None else None
        self.search_terms = self.generate_search_terms()

    def __eq__(self, other: Any) -> bool:
        return self.event_id == other.event_id

    def __hash__(self) -> int:
        return hash(self.event_id)

    def generate_search_terms(self) -> List[str]:
        search_terms = DatastoreUtils.split_term(self.title) + DatastoreUtils.split_term(self.description)
        search_terms = [re.sub(r'[^\w]+', '', term.lower()) for term in search_terms if len(term) > 3]
        if self.venue.search_terms is not None:
            search_terms.extend(self.venue.search_terms)
        return [term for term in search_terms if len(term) > 3]

    def __repr__(self) -> str:
        return f'core.Event {self.url} {self.title} {self.description}'

    @staticmethod
    def is_not_empty(text: str) -> bool:
        return text is not None and text != ''

    def is_valid(self) -> bool:
        valid = (Event.is_not_empty(self.title) and
                 Event.is_not_empty(self.description) and
                 self.when != datetime.min and
                 self.when > datetime.now(pytz.timezone(self.venue.timezone)) and
                 Event.is_not_empty(self.url))
        if not valid:
            logging.getLogger(__name__).warning('Invalid event %s', self)
        return valid
