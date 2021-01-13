from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_simplon_groningen_sync_from_html(simplon: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/simplon-groningen")
    sync_venues()

    assert repositories.event_repository.count() == 29

    event = repositories.event_repository.store[url_to_id("http://simplon.nl/?post_type=events&p=17602")]
    assert event.title == "Foxlane + Car Pets"
    assert event.description == "Simplon UP"
    assert event.image_url == "https://simplon.nl/content/uploads/2019/03/FOXLANE-MAIN-PRESS-PHOTO-600x600.jpg"

    # assert general rules:
    repositories.event_repository.assert_events(simplon)
