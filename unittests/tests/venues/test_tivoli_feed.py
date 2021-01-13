from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories


def test_tivoli_sync_from_html(tivoli: Venue, repositories: MockRepositories):

    # Set up syncing venues from vera venue
    repositories.set_directory_for_mock_client_session("tests/samples/tivoli-utrecht")

    sync_venues()

    assert repositories.event_repository.count() == 37
    event = [
        event
        for event in repositories.event_repository.store.values()
        if event.url == "https://www.tivolivredenburg.nl/agenda/worry-dolls-11-11-2019/"
    ][0]
    assert event.venue.venue_id == tivoli.venue_id
    assert event.title == "Worry Dolls"
    assert event.image_url == "https://www.tivolivredenburg.nl/wp-content/uploads/2019/05/Duo-Print-195x130.jpg"
    assert event.description == "Britse folk vol meerstemmige zang, banjo, ukulele, gitaar en mandoline"
    assert event.source == tivoli.source_url
    assert event.when.hour == 20
    assert event.when.minute == 30

    # assert general rules:
    repositories.event_repository.assert_events(tivoli)
