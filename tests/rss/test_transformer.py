import datetime
from datetime import datetime
from hamcrest import assert_that, equal_to, matches_regexp
from unittest.mock import MagicMock

from core.event import Event
from core.venue import Venue
from core.venue_repository import VenueRepository
from rss.transformer import Transformer


class TestTransformer:

    def test_as_xml(self):
        event = Event(url="http://klaasjan",
                      title='junit',
                      description='omschrijving',
                      venue_id='spot-groningen',
                      source='internet',
                      date_published=datetime.now(),
                      when=datetime.now(),
                      image_url='http://asdf')
        venue = Venue(
            venue_id='spot-groningen', name='spott',
            url='http://venue',
            city='Gron',
            country='NL', phone='yes',
            email='hotmail')
        venue_repository = VenueRepository()
        venue_repository.get_venue_for = MagicMock(return_value=venue)
        rss_item = Transformer().item_to_rss(venue_repository, event)
        assert_that(rss_item.title, equal_to('junit'))
        assert_that(rss_item.author, equal_to('internet'))
        assert_that(rss_item.guid, equal_to('http://klaasjan'))
        assert_that(rss_item.link, equal_to('http://klaasjan'))
        description = rss_item.description
        assert_that(description, matches_regexp('<p>omschrijving</p>'))
        assert_that(description, matches_regexp('Where: <a href="http://venue">spott \\(Gron, NL\\)</a></p>'))
        assert_that(description, matches_regexp('<p>When: \\d{4}-\\d\\d-\\d\\d \\d\\d:\\d\\d -'))
