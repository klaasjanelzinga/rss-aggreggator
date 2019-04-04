from xml.etree.ElementTree import Element

from hamcrest import assert_that, equal_to

from rss.item import RSSItem


class TestRSSChannel:

    def test_as_xml(self):
        rss_item = RSSItem(title='junit', link='http://dummy',
                           description='omschrijving',
                           author='junit', guid='unique',
                           source='the-truth')
        root = Element('root')
        rss_item.as_xml(root)
        assert_that(root.find('./item/title').text, equal_to('junit'))
        assert_that(root.find('./item/description').text, equal_to('omschrijving'))
        assert_that(root.find('./item/link').text, equal_to('http://dummy'))
        assert_that(root.find('./item/author').text, equal_to('junit'))
        assert_that(root.find('./item/source').text, equal_to('the-truth'))
        assert_that(root.find('./item/guid').text, equal_to('unique'))

