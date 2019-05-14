import unittest

from hamcrest import none, is_not
from hamcrest.core import assert_that

from venues.vera_groningen.vera_fetcher import VeraFetcher


class TestVeraGroningenFetcher(unittest.TestCase):

    def test_sample_file(self):
        fetcher = VeraFetcher()
        result = fetcher.fetch(1, 20)
        assert_that(result, is_not(none()))
