from xml.etree import ElementTree

from hamcrest import assert_that, equal_to

from app.rss.rss_item import RSSItem


def test_as_xml():
    rss_item = RSSItem(
        title="junit",
        link="http://dummy",
        description="omschrijving",
        author="junit",
        guid="unique",
        source="the-truth",
    )
    root = ElementTree.fromstring(rss_item.as_node())
    assert_that(root.find("./title").text, equal_to("junit"))
    assert_that(root.find("./description").text, equal_to("omschrijving"))
    assert_that(root.find("./link").text, equal_to("http://dummy"))
    assert_that(root.find("./author").text, equal_to("junit"))
    assert_that(root.find("./source").text, equal_to("the-truth"))
    assert_that(root.find("./guid").text, equal_to("unique"))
