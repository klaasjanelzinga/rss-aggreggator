import unittest

from hamcrest import matches_regexp
from hamcrest.core import assert_that

from app.core.data_fixer import DataFixer


class TestDataFixer(unittest.TestCase):

    def setUp(self) -> None:
        self.data_fixer = DataFixer()

    def test_random_future_date(self):
        result = self.data_fixer.fix('"date": "{{random_future_date:timestamp}}"')
        assert_that(result, matches_regexp(r'"date": "\d{10}"'))

    def test_random_future_date_pattern(self):
        result = self.data_fixer.fix('"date": "{{random_future_date:%d.%m.%Y}}  "')
        assert_that(result, matches_regexp(r'"date": "\d{2}\.\d{2}.\d{4}  "'))

    def test_random_future_time_pattern(self):
        result = self.data_fixer.fix('"date": "{{random_future_date:%H:%M:%S}}  "')
        assert_that(result, matches_regexp(r'"date": "\d{2}\:\d{2}:\d{2}  "'))

    def test_random_future_date_time_pattern(self):
        result = self.data_fixer.fix('"date": "{{random_future_date:%d.%m.%YT%H:%M}}  "')
        assert_that(result, matches_regexp(r'"date": "\d{2}\.\d{2}.\d{4}T\d{2}:\d{2}  "'))

    def test_simplon_pattern(self):
        result = self.data_fixer.fix('datum {{random_future_date:simplon-groningen}}')
        assert_that(result, matches_regexp(r'\w+ \d+ \w+ \d{4}'))

    def test_tivoli_pattern(self):
        result = self.data_fixer.fix('{{random_future_date:tivoli}}')
        assert_that(result, matches_regexp(r'"day": "\w{2} \d+", "month": "\w+", "year": "\d{4}",'))
