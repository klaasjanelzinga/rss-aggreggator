class VeraConfig:

    def __init__(self,
                 base_url='https://www.vera-groningen.nl',
                 source_url='https://www.vera-groningen.nl/programma/'):
        self.base_url = base_url
        self.source = source_url
        self.venue_id = 'vera-groningen'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'
