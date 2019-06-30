from app.core.event_repository import EventRepository
from app.core.source import Source
from app.core.venue import Venue
from app.core.venue_processor import VenueProcessor
from app.core.venue_repository import VenueRepository
from app.venues.melkweg_amsterdam.melkweg_source import MelkwegSource


class MelkwegProcessor(VenueProcessor):

    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = MelkwegProcessor.create_venue()
        venue_repository.register(self.venue)
        super().__init__(event_repository, self.venue)

    def fetch_source(self) -> Source:
        return MelkwegSource(self.venue)

    @staticmethod
    def create_venue() -> Venue:
        return Venue(venue_id='melkweg-amsterdam',
                     name='Melkweg Amsterdam',
                     phone='',
                     city='Amsterdam',
                     country='NL',
                     timezone='Europe/Amsterdam',
                     timezone_short='+02:00',
                     email='info@melkweg.nl',
                     source_url='https://www.melkweg.nl/agenda',
                     url='https://www.melkweg.nl')
