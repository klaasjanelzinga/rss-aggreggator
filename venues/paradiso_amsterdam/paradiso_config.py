from core.venue import Venue


class ParadisoConfig:

    def __init__(self,
                 base_url='https://www.paradiso.nl',
                 source_url='https://www.paradiso.nl/'):
        self.base_url = base_url
        self.source_url = source_url
        self.venue_id = 'paradiso-amsterdam'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'

    def venue(self) -> Venue:
        return Venue(venue_id=self.venue_id,
                     name='Paradiso Amsterdam',
                     phone='',
                     city='Amsterdam',
                     country='NL',
                     timezone='Europe/Amsterdam',
                     email='info@paradiso.nl',
                     url=self.base_url)
