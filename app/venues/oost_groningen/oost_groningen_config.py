from app.core.venue import Venue


class OostGroningenConfig:

    def __init__(self, base_url: str = 'https://www.komoost.nl'):
        self.venue_id = 'oost-groningen'
        self.base_url = base_url
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'

    def venue(self) -> Venue:
        return Venue(venue_id=self.venue_id,
                     name='Oost Groningen',
                     phone='',
                     city='Groningen',
                     country='NL',
                     timezone=self.timezone,
                     email='info@komoost.nl',
                     url=self.base_url)
