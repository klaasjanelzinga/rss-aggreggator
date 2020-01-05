from xml.etree import ElementTree

from hamcrest import equal_to
from hamcrest.core import assert_that
import pytest


@pytest.mark.asyncio
async def test_events_xml(client_session, backend_url):
    result = await client_session.get(f"{backend_url}/events.xml")
    assert_that(result.status, equal_to(200))
    root = ElementTree.fromstring(await result.text())
    assert_that(len(root), equal_to(1))
    assert_that(root.tag, equal_to("rss"))
    channel = root[0]
    assert_that(channel.tag, equal_to("channel"))
    for child in channel:
        if child.tag == "title":
            assert_that(child.text, equal_to("Events from all venues"))
        if child.tag == "link":
            assert_that(child.text, equal_to("https://rss-aggregator-236707.appspot.com"))
        if child.tag == "description":
            assert_that(child.text, equal_to("Aggregation of several venues"))
        if child.tag == "webMaster":
            assert_that(child.text, equal_to("klaasjanelzinga@gmail.com"))
        if child.tag == "managingEditor":
            assert_that(child.text, equal_to("klaasjanelzinga@gmail.com"))
        if child.tag == "generator":
            assert_that(child.text, equal_to("Python3"))
        if child.tag == "category":
            assert_that(child.text, equal_to("Entertainment"))
