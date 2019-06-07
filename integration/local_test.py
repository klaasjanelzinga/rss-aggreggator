from xml.etree import ElementTree

import requests
from hamcrest import equal_to
from hamcrest.core import assert_that

GREEN = '\033[92m'
END = '\033[0m'


def validate(url: str) -> None:
    response = requests.get(url)
    if response.status_code > 200:
        raise Exception(f'Should validate url {url} failed with status {response.status_code} - {response.content}')
    print(f'[{GREEN}OK{END}] url {url} validated')


def should_fail(url: str, expected_status: int) -> None:
    response = requests.get(url)
    if response.status_code != expected_status:
        raise Exception(f'Expected status code {expected_status} but was {response.status_code}')
    print(f'[{GREEN}OK{END}] url {url} should fail failed as expected')


validate('http://localhost:8080/events.xml')
validate('http://localhost:8080/maintenance/cleanup')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=spot-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=vera-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=simplon-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=oost-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=tivoli-utrecht')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=paradiso-amsterdam')
validate('http://localhost:8080')
validate('http://localhost:8080/api/events')
validate('http://localhost:8080/channel-image.png')

should_fail('http://localhost:8080/maintenance/fetch-data?venue_id=kumbatcha-groningen', 404)

result = requests.get('http://localhost:8080/events.xml')
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

assert_that(len(channel), equal_to(185))
print(f'[{GREEN}OK{END}] xml valid')
