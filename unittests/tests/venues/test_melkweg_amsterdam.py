from core_lib.application_data import sync_venues
from core_lib.core.models import Venue
from tests.mock_repositories import MockRepositories, url_to_id


def test_melkweg_amsterdam_sync_from_html(melkweg: Venue, repositories: MockRepositories):

    repositories.set_directory_for_mock_client_session("tests/samples/melkweg-amsterdam")
    sync_venues()

    assert repositories.event_repository.count() == 46
    event = repositories.event_repository.store[url_to_id("https://www.melkweg.nl/nl/agenda/olga-gartland-10-11-2019")]
    assert event.title == "Orla Gartland"
    assert event.description == (
        """De Ierse songer-songwriter Orla Gartland bewandelt het inmiddels bekende muziekpad voor de nieuwe generatie. Ze verzamelde in een korte tijd een flinke berg trouwe fans met haar zelfgeschreven songs op Youtube. Haar vrolijke feelgood pop past perfect bij de omschrijving die ze zichzelf geeft: een "music makin' ginger nutcase". Naast haar eigen video's schittert ze vaak in die van haar Youtube-collega Dodie en tourde ze met haar mee, onder andere bij haar concert hier in Amsterdam afgelopen februari. Haar nieuwe EP 'Why Am I Like This' is vers van de pers en ze kan niet wachten die live aan haar fans te laten horen!"""
    )
    assert (
        event.image_url
        == "https://s3-eu-west-1.amazonaws.com/static.melkweg.nl/uploads/images/scaled/agenda_thumbnail/25601"
    )

    # assert general rules:
    repositories.event_repository.assert_events(melkweg)
