class SpotConfig:

    def __init__(self,
                 base_url='https://www.spotgroningen.nl',
                 source_url='https://www.spotgroningen.nl/programma'):
        self.base_url = base_url
        self.source_url = source_url
        self.venue_id = 'spot-groningen'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'
