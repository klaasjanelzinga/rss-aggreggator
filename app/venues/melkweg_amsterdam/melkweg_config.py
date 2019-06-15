from app.core.venue import Venue


class MelkwegConfig:

    def __init__(self,
                 base_url='https://www.melkweg.nl',
                 source_url='https://www.melkweg.nl/agenda'):
        self.base_url = base_url
        self.source_url = source_url
        self.venue_id = 'melkweg-amsterdam'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'

    def venue(self) -> Venue:
        return Venue(venue_id=self.venue_id,
                     name='Melkweg Amsterdam',
                     phone='',
                     city='Amsterdam',
                     country='NL',
                     timezone='Europe/Amsterdam',
                     email='info@melkweg.nl',
                     url=self.base_url)
