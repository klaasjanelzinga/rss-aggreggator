class VeraConfig:

    def __init__(self,
                 base_url='https://www.vera-groningen.nl',
                 source_url='https://www.vera-groningen.nl/programma/',
                 scrape_url='https://www.vera-groningen.nl/wp/wp-admin/admin-ajax.php?action=renderProgramme&category=all&page={}&perpage={}&lang=nl'):
        self.base_url = base_url
        self.source = source_url
        self.scrape_url = scrape_url
        self.venue_id = 'vera-groningen'
