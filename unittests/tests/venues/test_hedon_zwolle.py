from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_hedon_zwolle_sync_from_html(hedon: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/hedon-zwolle")
    sync_venues()

    # Fix time in #programma -> parse from datetime="2019-08-29" ie text.
    assert repositories.event_repository.count() == 105
    event = repositories.event_repository.store[url_to_id("https://www.hedon-zwolle.nl/voorstelling/30455/de-kift-")]
    assert event.title == "DE KIFT "
    assert event.description == "DE KIFT "
    assert event.image_url is None

    # assert general rules:
    repositories.event_repository.assert_events(hedon)
