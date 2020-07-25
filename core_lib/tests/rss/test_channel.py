from xml.etree import ElementTree

from hamcrest import assert_that, equal_to, is_not, none

from core_lib.rss.channel import RSSChannel


def test_as_xml():
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
