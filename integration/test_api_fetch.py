import base64
import unittest

import requests
from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from integration.integration_utils import with_url


class TestApiFetch(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint = 'http://localhost:8080'
        with_url(f'{self.endpoint}/maintenance/ping')

    def test_first_fetch(self):
        result = requests.get(f'{self.endpoint}/api/events', params={
            'fetch_offset': ''
        })
        assert_that(result.status_code, equal_to(200))
        assert_that(len(result.json()['events']), equal_to(25))
        token: str = result.json()['fetch_offset']
        assert_that(base64.decodebytes(token.encode('utf-8')).decode('utf-8'), is_not(equal_to('DONE')))

    def test_paging(self):
        result = requests.get(f'{self.endpoint}/api/events', params={
            'fetch_offset': ''
        })
        assert_that(result.status_code, equal_to(200))
        json = result.json()
        assert_that(len(json['events']), equal_to(25))
        first_event_id = json['events'][0]['id']
        token: str = result.json()['fetch_offset']
        result = requests.get(f'{self.endpoint}/api/events', params={
            'fetch_offset': token
        })
        assert_that(result.status_code, equal_to(200))
        json = result.json()
        assert_that(len(json['events']), equal_to(25))
        second_event_id = json['events'][0]['id']
        assert_that(first_event_id, is_not(equal_to(second_event_id)))
