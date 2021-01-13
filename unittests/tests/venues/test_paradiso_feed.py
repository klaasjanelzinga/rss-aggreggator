from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_paradiso_amsterdam_sync_from_html(paradiso: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/paradiso-amsterdam")
    sync_venues()

    assert repositories.event_repository.count() == 35

    event = repositories.event_repository.store[
        url_to_id("https://www.paradiso.nl/en/program/cropfest-40-jaar-eton-crop-40-jaar-diy/60445/")
    ]
    assert event.title == "CROPFEST \u2013 40 jaar Eton Crop, 40 jaar DIY"
    assert event.description == "Met o.a. EC Groove Society, Quazar en Joost van Bellen"
    assert event.image_url == "https://api.paradiso.nl/img/events//cropfest_2019.JPG"

    # assert general rules:
    repositories.event_repository.assert_events(paradiso)
