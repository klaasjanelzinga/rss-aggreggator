import unittest

from hamcrest import assert_that, equal_to, matches_regexp

from rss.transformer import Transformer
from tests.core.fixtures import fixture_vera_event


class TestTransformer(unittest.TestCase):

    def test_as_xml(self):
        event = fixture_vera_event()
        rss_item = Transformer().item_to_rss(event)
        assert_that(rss_item.title, equal_to('Vera Event titel'))
        assert_that(rss_item.author, equal_to('vera'))
        assert_that(rss_item.guid, equal_to('http://dummy-vera-event'))
        assert_that(rss_item.link, equal_to('http://dummy-vera-event'))
        description = rss_item.description
        assert_that(description, matches_regexp('<p>Omschrijving</p>'))
        assert_that(description, matches_regexp(
            'Where: <a href="http://venue-url-vera-groningen">VERA-Groningen .Groningen, NL.</a></p>'))
        assert_that(description, matches_regexp('<p>When: \\d{4}-\\d\\d-\\d\\d \\d\\d:\\d\\d -'))
