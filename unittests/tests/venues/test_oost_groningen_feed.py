from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_oost_groningen_sync_from_html(oost: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/oost-groningen")
    sync_venues()

    assert repositories.event_repository.count() == 8
    event = repositories.event_repository.store[url_to_id("https://www.facebook.com/events/610421539383220/")]
    assert event.title == "HOMOOST • Movie Night: Party Monster the Shockumentary"
    assert event.description == "Movie Screening • Group Discussion"
    assert event.image_url == "https://www.komoost.nl/media/56721601_1992667177522931_8267801960216788992_o.jpg"

    # assert general rules:
    repositories.event_repository.assert_events(oost)
