from datetime import datetime

from core.event import Event
from core.venue import Venue


def fixture_vera_event() -> Event:
    return Event(url='http://dummy-vera-event',
                 description='Omschrijving',
                 title='Vera Event titel',
                 source='vera',
                 date_published=datetime.now(),
                 image_url='http://image-url-vera-event.jpg',
                 venue=fixture_vera_venue(),
                 when=datetime.now())


def fixture_vera_event_mock() -> Event:
    return Event(url='http://dummy-vera-event-mock',
                 description='Omschrijving vera event mock',
                 title='Vera Event titel mock',
                 source='vera',
                 date_published=datetime.now(),
                 image_url='http://image-url-vera-event-mock.jpg',
                 venue=fixture_vera_venue(),
                 when=datetime.now())


def fixture_vera_venue() -> Venue:
    return Venue(venue_id='vera-groningen',
                 name='VERA-Groningen',
                 phone='+31 (0)50 313 46 81',
                 city='Groningen',
                 country='NL',
                 timezone='Europe/Amsterdam',
                 email='info@vera-groningen.nl',
                 url='http://venue-url-vera-groningen')

