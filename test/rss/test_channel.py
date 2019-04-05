from xml.etree import ElementTree

from hamcrest import none, is_not, assert_that, equal_to

from rss.channel import RSSChannel
from rss.rss_item import RSSItem


class TestRSSChannel:

    def test_as_xml(self):
        rss_item = RSSItem(title='junit', link='http://dummy',
                           description='omschrijving',
                           author='junit', guid='unique',
                           source='the-truth')
        channel = RSSChannel([rss_item])
        as_xml = channel.as_xml()
        assert_that(as_xml, is_not(none()))
        root = ElementTree.fromstring(as_xml)
        channel = root.findall('channel')
        assert_that(len(channel), equal_to(1))
        assert_that(channel[0].find('title').text, equal_to('Events aggregator'))
        parsed_items = root.findall('./channel/item')
        assert_that(len(parsed_items), equal_to(1))


