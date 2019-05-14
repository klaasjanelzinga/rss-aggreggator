from dataclasses import dataclass
from datetime import datetime

from babel.dates import get_timezone

from core.datastore_utils import DatastoreUtils


@dataclass
class Venue:

    name: str
    url: str
    venue_id: str
    email: str
    phone: str
    city: str
    country: str
    timezone: str

    def __post_init__(self):
        self.search_terms = [term.lower() for term in DatastoreUtils.split_term(self.name) + [self.city]]

    def convert_utc_to_venue_timezone(self, when: datetime) -> datetime:
        venue_tz = get_timezone(self.timezone)
        return when.astimezone(venue_tz)
