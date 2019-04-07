import datetime
from datetime import datetime

from hamcrest import assert_that, equal_to

from core.event import Event
from core.venue_repository import VenueRepository
from rss.transformer import Transformer
from spot.processor import SpotProcessor


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
        venue_repository = VenueRepository()
        spot_processor = SpotProcessor(None)
        spot_processor.register_venue_at(venue_repository)
        rss_item = Transformer().item_to_rss(venue_repository, event)
        assert_that(rss_item.title, equal_to('junit'))
        assert_that(rss_item.author, equal_to('internet'))
        assert_that(rss_item.guid, equal_to('http://klaasjan'))
        assert_that(rss_item.link, equal_to('http://klaasjan'))
