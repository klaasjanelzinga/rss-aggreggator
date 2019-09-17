from datetime import datetime, timedelta

import pytz

from app.core.event import Event
from app.core.venue.venue import Venue


def fixture_vera_event() -> Event:
    return Event(url='http://dummy-vera-event',
                 description='Omschrijving',
                 title='Vera Event titel',
                 source='vera',
                 date_published=datetime.now(),
                 image_url='http://image-url-vera-event.jpg',
                 venue=fixture_vera_venue(),
                 when=datetime.now(pytz.timezone('Europe/Amsterdam')) + timedelta(days=10))


def fixture_vera_event_mock() -> Event:
    return Event(url='http://dummy-vera-event-mock',
                 description='Omschrijving vera event mock',
                 title='Vera Event titel mock',
                 source='vera',
                 date_published=datetime.now(),
                 image_url='http://image-url-vera-event-mock.jpg',
                 venue=fixture_vera_venue(),
                 when=datetime.now(pytz.timezone('Europe/Amsterdam')) + timedelta(days=10))


def fixture_vera_venue() -> Venue:
    return Venue(venue_id='vera-groningen',
                 name='VERA-Groningen',
                 short_name='Vera NL-GRN',
                 phone='+31 (0)50 313 46 81',
                 city='Groningen',
                 country='NL',
                 timezone='Europe/Amsterdam',
                 timezone_short='+02:00',
                 email='info@vera-groningen.nl',
                 source_url='http://venue-url-vera-groningen',
                 url='http://venue-url-vera-groningen')
