from app.core.venue import Venue


class VeraConfig:

    def __init__(self,
                 base_url='https://www.vera-groningen.nl',
                 source_url='https://www.vera-groningen.nl/programma/'):
        self.base_url = base_url
        self.source = source_url
        self.venue_id = 'vera-groningen'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'

    def venue(self) -> Venue:
        return Venue(venue_id=self.venue_id,
                     name='VERA-Groningen',
                     phone='+31 (0)50 313 46 81',
                     city='Groningen',
                     country='NL',
                     timezone=self.timezone,
                     email='info@vera-groningen.nl',
                     url=self.base_url)
