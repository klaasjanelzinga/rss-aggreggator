from core.venue import Venue


class SpotConfig:

    def __init__(self,
                 base_url='https://www.spotgroningen.nl',
                 source_url='https://www.spotgroningen.nl/programma'):
        self.base_url = base_url
        self.source_url = source_url
        self.venue_id = 'spot-groningen'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'

    def venue(self) -> Venue:
        return Venue(venue_id=self.venue_id,
                     name='SPOT',
                     phone='+31 (0)50-3680111',
                     city='Groningen',
                     country='NL',
                     timezone='Europe/Amsterdam',
                     email='info@spotgroningen.nl',
                     url=self.base_url)
