from hamcrest import assert_that, equal_to
from lxml.etree import fromstring

from core_lib.core.rss import RSSItem


def test_as_xml():
    rss_item = RSSItem(
        title="junit",
        link="http://dummy",
        description="omschrijving",
        author="junit",
        guid="unique",
        pub_date="Thu, 20 Sep 2020 13:14:15 +0000",
        source="the-truth",
    )
    root = fromstring(rss_item.as_node())
    assert_that(root.find("./title").text, equal_to("junit"))
    assert_that(root.find("./description").text, equal_to("omschrijving"))
    assert_that(root.find("./link").text, equal_to("http://dummy"))
    assert_that(root.find("./author").text, equal_to("junit"))
    assert_that(root.find("./source").text, equal_to("the-truth"))
    assert_that(root.find("./guid").text, equal_to("unique"))
