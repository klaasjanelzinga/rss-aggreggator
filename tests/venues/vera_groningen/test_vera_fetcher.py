from datetime import datetime, tzinfo

import dateparser
from hamcrest import equal_to, matches_regexp, none, is_not
from hamcrest.core import assert_that

from venues.vera_groningen.vera_fetcher import VeraFetcher
from venues.vera_groningen.vera_parser import VeraParser
from venues.vera_groningen.vera_config import VeraConfig


class TestVeraGroningenFetcher:

    def test_sample_file(self):
        fetcher = VeraFetcher()
        result = fetcher.fetch(1, 20)
        assert_that(result, is_not(none()))
