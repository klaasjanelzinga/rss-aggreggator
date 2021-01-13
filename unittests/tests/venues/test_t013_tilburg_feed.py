from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_t013_sync_from_html(t013: Venue, repositories: MockRepositories):

    # Set up syncing venues from vera venue
    repositories.set_directory_for_mock_client_session("tests/samples/t013-tilburg")

    sync_venues()

    assert repositories.event_repository.count() == 7

    event = repositories.event_repository.store[url_to_id("https://www.013.nl/programma/5423/snelle")]
    assert event.description == "Tot op de reu00fcnie!"
    assert event.image_url == "https://www.013.nl/uploads/cache/event_main_mobile/5d7febc5306f2.jpg?version=1568700682"
    assert event.title == "Snelle + Pjotr"

    # assert general rules:
    repositories.event_repository.assert_events(t013)
