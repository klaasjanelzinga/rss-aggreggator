from app.core.venue import Venue


class SimplonConfig:

    def __init__(self, base_url: str = 'https://www.simplon.nl'):
        self.venue_id = 'simplon-groningen'
        self.base_url = base_url
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'

    def venue(self) -> Venue:
        return Venue(venue_id=self.venue_id,
                     name='Simplon Groningen',
                     phone='0503184150',
                     city='Groningen',
                     country='NL',
                     timezone=self.timezone,
                     email='info@simplon.nl',
                     url=self.base_url)
