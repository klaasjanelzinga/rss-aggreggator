from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue.venue import Venue
from app.core.venue.venue_processor import VenueProcessor
from app.core.venue.venue_repository import VenueRepository
from app.venues.simplon_groningen.simplon_source import SimplonSource


class SimplonProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = SimplonProcessor.create_venue()
        venue_repository.register(self.venue)
        super().__init__(event_repository, self.venue)

    def fetch_source(self) -> Source:
        return SimplonSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(venue_id='simplon-groningen',
                     name='Simplon Groningen',
                     phone='0503184150',
                     city='Groningen',
                     country='NL',
                     timezone='Europe/Amsterdam',
                     timezone_short='+02:00',
                     email='info@simplon.nl',
                     source_url='https://www.simplon.nl/agenda',
                     url='https://www.simplon.nl')
