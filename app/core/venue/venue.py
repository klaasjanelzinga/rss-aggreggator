from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from babel.dates import get_timezone

from app.core.datastore_utils import DatastoreUtils


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
    last_fetched_date: datetime = datetime.now()
    search_terms: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.search_terms = [term.lower() for term in DatastoreUtils.split_term(self.name) + [self.city]]

    def convert_utc_to_venue_timezone(self, when: datetime) -> datetime:
        venue_tz = get_timezone(self.timezone)
        return when.astimezone(venue_tz)
