import unittest
from xml.etree import ElementTree

from hamcrest import none, is_not, assert_that, equal_to

from app.rss.channel import RSSChannel


class TestRSSChannel(unittest.TestCase):
    def test_as_xml(self):
        channel = RSSChannel()
        as_xml = channel.generate_pre_amble()
        assert_that(as_xml, is_not(none()))
        root = ElementTree.fromstring(as_xml)
        channel = root.findall("channel")
        assert_that(len(channel), equal_to(1))
        assert_that(channel[0].find("title").text, equal_to("Events from all venues"))
        assert_that(len(root.findall("./channel/image")), equal_to(1))
        assert_that(root.find("./channel/image/title").text, equal_to("Events from all venues"))
        assert_that(root.find("./channel/image/url").text, is_not(none()))
        assert_that(root.find("./channel/image/link").text, is_not(none()))
        assert_that(root.find("./channel/webMaster").text, equal_to("klaasjanelzinga@gmail.com"))
        assert_that(root.find("./channel/managingEditor").text, equal_to("klaasjanelzinga@gmail.com"))
        assert_that(root.find("./channel/managingEditor").text, equal_to("klaasjanelzinga@gmail.com"))
        assert_that(root.find("./channel/generator").text, equal_to("Python3"))
