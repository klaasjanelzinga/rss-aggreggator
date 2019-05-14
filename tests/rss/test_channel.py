import unittest

from hamcrest import none, is_not, assert_that, equal_to
from xml.etree import ElementTree

from rss.channel import RSSChannel
from rss.rss_item import RSSItem


class TestRSSChannel(unittest.TestCase):

    def test_as_xml(self):
        rss_item = RSSItem(title='junit', link='http://dummy',
                           description='omschrijving',
                           author='junit', guid='unique',
                           source='the-truth')
        channel = RSSChannel([rss_item])
        as_xml = channel.to_xml()
        assert_that(as_xml, is_not(none()))
        root = ElementTree.fromstring(as_xml)
        channel = root.findall('channel')
        assert_that(len(channel), equal_to(1))
        assert_that(channel[0].find('title').text, equal_to('Events from all venues'))
        parsed_items = root.findall('./channel/item')
        assert_that(len(parsed_items), equal_to(1))
        assert_that(len(root.findall('./channel/image')), equal_to(1))
        assert_that(root.find('./channel/image/title').text, equal_to('Events from all venues'))
        assert_that(root.find('./channel/image/url').text, is_not(none()))
        assert_that(root.find('./channel/image/link').text, is_not(none()))
        assert_that(root.find('./channel/webMaster').text, equal_to('klaasjanelzinga@gmail.com'))
        assert_that(root.find('./channel/managingEditor').text, equal_to('klaasjanelzinga@gmail.com'))
        assert_that(root.find('./channel/managingEditor').text, equal_to('klaasjanelzinga@gmail.com'))
        assert_that(root.find('./channel/generator').text, equal_to('Python3'))



