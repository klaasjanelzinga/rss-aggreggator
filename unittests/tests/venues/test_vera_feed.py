from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_vera_sync_from_html(vera: Venue, repositories: MockRepositories):

    # Set up syncing venues from vera venue
    repositories.set_directory_for_mock_client_session("tests/samples/vera-groningen")

    sync_venues()

    assert repositories.event_repository.count() == 39

    event = repositories.event_repository.store[
        url_to_id("http://www.vera-groningen.nl/?post_type=events&p=107558&lang=nl")
    ]
    assert event.title == "Meadowlake (GRN) (VERPLAATST NAAR)"
    assert event.description == "Meadowlake (GRN)"
    assert event.image_url == "https://www.vera-groningen.nl/content/uploads/2020/10/meadow2400-360x250.jpg"

    # assert general rules:
    repositories.event_repository.assert_events(vera)
