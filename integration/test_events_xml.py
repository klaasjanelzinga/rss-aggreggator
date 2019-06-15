import unittest
from xml.etree import ElementTree

import requests
from hamcrest import equal_to
from hamcrest.core import assert_that

from integration.integration_utils import with_url


class TestEventsXml(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint = 'http://localhost:8080'
        with_url(f'{self.endpoint}/maintenance/ping')

    def test_events_xml(self):
        result = requests.get(f'{self.endpoint}/events.xml')
        assert_that(result.status_code, equal_to(200))
        root = ElementTree.fromstring(result.content)
        assert_that(len(root), equal_to(1))
        assert_that(root.tag, equal_to('rss'))
        channel = root[0]
        assert_that(channel.tag, equal_to('channel'))
        for child in channel:
            if child.tag == 'title':
                assert_that(child.text, equal_to('Events from all venues'))
            if child.tag == 'link':
                assert_that(child.text, equal_to('https://rss-aggregator-236707.appspot.com'))
            if child.tag == 'description':
                assert_that(child.text, equal_to('Aggregation of several venues'))
            if child.tag == 'webMaster':
                assert_that(child.text, equal_to('klaasjanelzinga@gmail.com'))
            if child.tag == 'managingEditor':
                assert_that(child.text, equal_to('klaasjanelzinga@gmail.com'))
            if child.tag == 'generator':
                assert_that(child.text, equal_to('Python3'))
            if child.tag == 'category':
                assert_that(child.text, equal_to('Entertainment'))

        assert_that(len(channel), equal_to(231))
