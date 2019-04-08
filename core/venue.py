from datetime import datetime

from babel.dates import get_timezone


class Venue:

    def __init__(self, venue_id: str,
                 name: str,
                 url: str,
                 city: str,
                 country: str,
                 timezone: str,
                 phone: str,
                 email: str):
        self.name = name
        self.url = url
        self.venue_id = venue_id
        self.email = email
        self.phone = phone
        self.city = city
        self.country = country
        self.timezone = timezone

    def convert_utc_to_venue_timezone(self, when: datetime) -> datetime:
        venue_tz = get_timezone(self.timezone)
        return when.astimezone(venue_tz)
