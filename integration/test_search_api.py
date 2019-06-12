import base64
import unittest

import requests
from hamcrest import equal_to
from hamcrest.core import assert_that

from integration.integration_utils import with_url


class TestSearchApi(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint = 'http://localhost:8080'
        with_url(f'{self.endpoint}/maintenance/ping')

    def test_single_result(self):
        result = requests.get(f'{self.endpoint}/api/search', params={
            'term': 'Beyond Hip Hop with support A Lecture By Rich Medina'
        })
        assert_that(result.status_code, equal_to(200))
        assert_that(len(result.json()['events']), equal_to(1))
        token: str = result.json()['fetch_offset']
        assert_that(base64.decodebytes(token.encode('utf-8')).decode('utf-8'), equal_to('DONE'))

    def test_none_result(self):
        result = requests.get(f'{self.endpoint}/api/search', params={
            'term': 'klaasjanelzingapython37'
        })
        assert_that(result.status_code, equal_to(200))
        assert_that(len(result.json()['events']), equal_to(0))
        token: str = result.json()['fetch_offset']
        assert_that(base64.decodebytes(token.encode('utf-8')).decode('utf-8'), equal_to('DONE'))

    def test_paging_result(self):
        done = False
        token = ''
        ite = 0
        tot_items = 0
        while not done:
            result = requests.get(f'{self.endpoint}/api/search', params={
                'term': 'groningen',
                'fetch_offset': token
            })
            ite += 1
            assert_that(result.status_code, equal_to(200))
            tot_items += len(result.json()['events'])
            token: str = result.json()['fetch_offset']
            done = base64.decodebytes(token.encode('utf-8')).decode('utf-8') == 'DONE'

        assert_that(ite, equal_to(5))
        assert_that(tot_items, equal_to(115))
