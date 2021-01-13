import pytest
import pytz
from aiohttp import ClientSession, ClientTimeout
from faker import Faker

from core_lib import application_data
from core_lib.application_data import Repositories, Processors
from core_lib.core.models import Event, Venue
from core_lib.core.repositories import EventEntityTransformer
from core_lib.core.user_profile import UserProfile
from core_lib.venues.hedon_zwolle import HedonProcessor
from core_lib.venues.melkweg_amsterdam import MelkwegProcessor
from core_lib.venues.neushoorn_leeuwarden import NeushoornProcessor
from core_lib.venues.oost_groningen import OostGroningenProcessor
from core_lib.venues.paradiso_amsterdam import ParadisoProcessor
from core_lib.venues.simplon_groningen import SimplonProcessor
from core_lib.venues.spot_groningen import SpotProcessor
from core_lib.venues.t013_tilburg import T013Processor
from core_lib.venues.tivoli_utrecht import TivoliProcessor
from core_lib.venues.vera_groningen import VeraProcessor
from tests.mock_repositories import MockRepositories

application_data.repositories = MockRepositories()
application_data.venue_processors = Processors(application_data.repositories)
application_data.event_entity_transformer = EventEntityTransformer(
    venue_repository=application_data.repositories.venue_repository
)


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def repositories() -> Repositories:
    repositories = application_data.repositories
    repositories.reset()
    return repositories


@pytest.fixture
def venue_processors(repositories: Repositories) -> Processors:
    return application_data.venue_processors


@pytest.fixture
def vera(repositories: Repositories) -> Venue:
    vera = VeraProcessor.create_venue()
    repositories.venue_repository.insert(vera)
    return vera


@pytest.fixture
def tivoli(repositories: Repositories) -> Venue:
    tivoli = TivoliProcessor.create_venue()
    repositories.venue_repository.insert(tivoli)
    return tivoli


@pytest.fixture
def t013(repositories: Repositories) -> Venue:
    t013 = T013Processor.create_venue()
    repositories.venue_repository.insert(t013)
    return t013


@pytest.fixture
def spot(repositories: Repositories) -> Venue:
    spot = SpotProcessor.create_venue()
    repositories.venue_repository.insert(spot)
    return spot


@pytest.fixture
def simplon(repositories: Repositories) -> Venue:
    simplon = SimplonProcessor.create_venue()
    repositories.venue_repository.insert(simplon)
    return simplon


@pytest.fixture
def paradiso(repositories: Repositories) -> Venue:
    paradiso = ParadisoProcessor.create_venue()
    repositories.venue_repository.insert(paradiso)
    return paradiso


@pytest.fixture
def oost(repositories: Repositories) -> Venue:
    oost = OostGroningenProcessor.create_venue()
    repositories.venue_repository.insert(oost)
    return oost


@pytest.fixture
def neushoorn(repositories: Repositories) -> Venue:
    neushoorn = NeushoornProcessor.create_venue()
    repositories.venue_repository.insert(neushoorn)
    return neushoorn


@pytest.fixture
def melkweg(repositories: Repositories) -> Venue:
    melkweg = MelkwegProcessor.create_venue()
    repositories.venue_repository.insert(melkweg)
    return melkweg


@pytest.fixture
def hedon(repositories: Repositories) -> Venue:
    hedon = HedonProcessor.create_venue()
    repositories.venue_repository.insert(hedon)
    return hedon


@pytest.fixture
def valid_venue(faker: Faker, repositories: Repositories) -> Venue:
    venue = Venue(
        venue_id=faker.name(),
        name=faker.name(),
        short_name=faker.sentence(),
        phone=faker.phone_number(),
        city=faker.city(),
        country=faker.country_code(),
        timezone="Europe/Amsterdam",
        email=faker.ascii_email(),
        source_url=faker.url(),
        url=faker.url(),
    )
    repositories.venue_repository.insert(venue)
    return venue


@pytest.fixture
def valid_event(faker: Faker, valid_venue: Venue) -> Event:
    return Event(
        url=faker.url(),
        description=faker.sentence(),
        title=faker.sentence(),
        source=valid_venue.source_url,
        date_published=faker.past_date(start_date="-1d", tzinfo=pytz.timezone("Europe/Amsterdam")),
        image_url=faker.uri(),
        venue=valid_venue,
        when=faker.date_time_this_year(before_now=False, after_now=True, tzinfo=pytz.timezone("Europe/Amsterdam")),
    )


@pytest.fixture
def valid_user_profile(faker: Faker) -> UserProfile:
    return UserProfile(
        email=faker.ascii_email(), given_name=faker.first_name(), family_name=faker.last_name(), avatar_url=faker.uri()
    )


@pytest.fixture
async def client_session():
    timeout = ClientTimeout(40)
    a_client_session = ClientSession(timeout=timeout)
    yield a_client_session
    await a_client_session.close()
