class TivoliConfig:

    def __init__(self,
                 base_url='https://www.tivolivredenburg.nl',
                 source_url='https://www.tivolivredenburg.nl/agenda/'):
        self.base_url = base_url
        self.source_url = source_url
        self.venue_id = 'tivoli-utrecht'
        self.timezone = 'Europe/Amsterdam'
        self.timezone_short = '+02:00'
