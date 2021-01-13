from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_spot_groningen_sync_from_html(spot: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/spot-groningen")
    sync_venues()

    assert repositories.event_repository.count() == 20

    event = repositories.event_repository.store[url_to_id("https://www.spotgroningen.nl/programma/kamagurka/")]
    assert event.description == "De overtreffende trap van absurditeit"
    assert event.image_url == (
        "https://www.spotgroningen.nl/wp-content/uploads/2019/02/"
        "Kamagurka-20-20De-20grenzen-20van-20de-20ernst-20"
        "Kamagurka-202-20300-20dpi-20RGB-150x150.jpg"
    )
    assert event.title == "Kamagurka - De grenzen van de ernst"

    # assert general rules:
    repositories.event_repository.assert_events(spot)
