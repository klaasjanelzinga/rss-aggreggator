import unittest

import requests
from hamcrest import equal_to
from hamcrest.core import assert_that

from integration.integration_utils import with_url


class TestEndpoints(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.endpoint = 'http://localhost:8080'
        with_url(f'{self.endpoint}/maintenance/ping')

    @staticmethod
    def validate(url: str) -> None:
        response = requests.get(url)
        assert_that(response.status_code, equal_to(200))

    def test_events_xml(self):
        TestEndpoints.validate(f'{self.endpoint}/events.xml')

    def test_cleanup(self):
        TestEndpoints.validate(f'{self.endpoint}/maintenance/cleanup')

    def test_maintenance(self):
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=spot-groningen')
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=vera-groningen')
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=simplon-groningen')
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=oost-groningen')
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=tivoli-utrecht')
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=paradiso-amsterdam')
        TestEndpoints.validate(f'{self.endpoint}/maintenance/fetch-data?venue_id=melkweg-amsterdam')
        response = requests.get(f'{self.endpoint}/maintenance/fetch-data?venue_id=kumbatcha-groningen')
        assert_that(response.status_code, equal_to(404))

    def test_root(self):
        TestEndpoints.validate(f'{self.endpoint}')

    def test_api_events(self):
        TestEndpoints.validate(f'{self.endpoint}/api/events')

    def test_api_search(self):
        TestEndpoints.validate(f'{self.endpoint}/api/search?term=groningen')

    def test_channel_image(self):
        TestEndpoints.validate(f'{self.endpoint}/channel-image.png')

    def test_user_profile(self):
        response = requests.get(f'{self.endpoint}/api/user/profile')
        assert_that(response.status_code, equal_to(404))
        response = requests.post(f'{self.endpoint}/api/user/profile', json={
            'email': 'klaasjanelzinga@test',
            'givenName': 'klaasajn',
            'familyName': 'elz'
        })
        assert_that(response.status_code, equal_to(404))
        response = requests.post(f'{self.endpoint}/api/user/signup', json={
            'email': 'klaasjanelzinga@test',
            'givenName': 'klaasajn',
            'familyName': 'elz'
        })
        assert_that(response.status_code, equal_to(404))
        response = requests.get(f'{self.endpoint}/api/user/profile', headers={
            'Authorization': 'Bearer 123123123123',
            'Accepts': 'application/json'
        })
        assert_that(response.status_code, equal_to(404))
        response = requests.get(f'{self.endpoint}/api/user/profile', headers={
            'Authorization': 'Bearer',
            'Accepts': 'application/json'
        })
        assert_that(response.status_code, equal_to(404))
        response = requests.get(f'{self.endpoint}/api/user/profile', headers={
            'Authorization': 'Beare',
            'Accepts': 'application/json'
        })
        assert_that(response.status_code, equal_to(404))


