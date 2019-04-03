from xml.etree import ElementTree

from hamcrest import none, is_not, assert_that, equal_to

from rss.channel_factory import ChannelFactory


class TestRSSChannel:

    def test_as_xml(self):
        channel = ChannelFactory.create_default_channel()
        xml = channel.as_xml()
        assert_that(xml, is_not(none()))
        root = ElementTree.fromstring(xml)
        channel = root.findall('channel')
        assert_that(len(channel), equal_to(1))
        assert_that(channel[0].find('title').text, equal_to('Events aggregator'))
