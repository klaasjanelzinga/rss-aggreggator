import requests


def validate(url: str) -> None:
    response = requests.get(url)
    if response.status_code > 200:
        raise Exception(f'Should validate url {url} failed with status {response.status_code} - {response.content}')
    print(f'[OK] url {url} validated')


def should_fail(url: str, expected_status:int) -> None:
    response = requests.get(url)
    if response.status_code != expected_status:
        raise Exception(f'Expected status code {expected_status} but was {response.status_code}')
    print(f'[OK] url {url} should fail failed as expected')


validate('http://localhost:8080/events.xml')
validate('http://localhost:8080/maintenance/cleanup')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=spot-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=vera-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=simplon-groningen')
validate('http://localhost:8080/maintenance/fetch-data?venue_id=oost-groningen')
validate('http://localhost:8080')
validate('http://localhost:8080/api/events')
validate('http://localhost:8080/channel-image.png')

should_fail('http://localhost:8080/maintenance/fetch-data?venue_id=kumbatcha-groningen', 404)
