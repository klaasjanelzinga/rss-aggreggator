import datetime
from datetime import datetime

from hamcrest import assert_that, equal_to

from core.event import Event
from rss.transformer import Transformer


class TestTransformer:

    def test_as_xml(self):
        event = Event(url="http://klaasjan",
                      title='junit',
                      description='omschrijving',
                      venue_id='oost',
                      source='internet',
                      date_published=datetime.now(),
                      when=datetime.now(),
                      image_url='http://asdf')
        rss_item = Transformer().item_to_rss(event)
        assert_that(rss_item.title, equal_to('junit'))
        assert_that(rss_item.author, equal_to('internet'))
        assert_that(rss_item.guid, equal_to('http://klaasjan'))
        assert_that(rss_item.link, equal_to('http://klaasjan'))
