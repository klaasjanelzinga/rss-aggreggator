from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_neushoorn_leeuwarden_sync_from_html(neushoorn: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/neushoorn-leeuwarden")
    sync_venues()

    assert repositories.event_repository.count() == 16
    event = repositories.event_repository.store[
        url_to_id("https://neushoorn.nl/production/uit-de-hoge-hoed-improv-comedy-11/")
    ]
    assert event.title == "Uit de Hoge Hoed: Improv Comedy"
    assert (
        event.description
        == "November 21, 2019 in Leeuwarden. Met Uit de Hoge Hoed lig je gegarandeerd de hele avond in een deuk! Doe&hellip;"
    )
    assert event.image_url == "https://neushoorn.nl/wp-content/uploads/2019/06/uit_de_hoge_hoed_front-2-1024x576.jpg"

    # assert general rules:
    repositories.event_repository.assert_events(neushoorn)
