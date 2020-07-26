from unittest.mock import Mock

import pytest
import pytz
from aiohttp import ClientSession, ClientTimeout
from faker import Faker

from core_lib.core.models import Event, Venue
from core_lib.core.user_profile import UserProfile
from core_lib.core.repositories import VenueRepository, EventRepository
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

FAKE = Faker()


@pytest.fixture
def mock_venue_repository() -> VenueRepository:
    return Mock(spec=VenueRepository)


@pytest.fixture
def mock_event_repository() -> EventRepository:
    return Mock(spec=EventRepository)


@pytest.fixture
def hedon_processor(mock_event_repository, mock_venue_repository) -> HedonProcessor:
    return HedonProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def melkweg_processor(mock_event_repository, mock_venue_repository) -> MelkwegProcessor:
    return MelkwegProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def neushoorn_processor(mock_event_repository, mock_venue_repository) -> NeushoornProcessor:
    return NeushoornProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def oost_processor(mock_event_repository, mock_venue_repository) -> OostGroningenProcessor:
    return OostGroningenProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def paradiso_processor(mock_event_repository, mock_venue_repository) -> ParadisoProcessor:
    return ParadisoProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def simplon_processor(mock_event_repository, mock_venue_repository) -> SimplonProcessor:
    return SimplonProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def spot_processor(mock_event_repository, mock_venue_repository) -> SpotProcessor:
    return SpotProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def t013_processor(mock_event_repository, mock_venue_repository) -> T013Processor:
    return T013Processor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def tivoli_processor(mock_event_repository, mock_venue_repository) -> TivoliProcessor:
    return TivoliProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def vera_processor(mock_event_repository, mock_venue_repository) -> VeraProcessor:
    return VeraProcessor(event_repository=mock_event_repository, venue_repository=mock_venue_repository,)


@pytest.fixture
def valid_venue() -> Venue:
    return Venue(
        venue_id=FAKE.name(),
        name=FAKE.name(),
        short_name=FAKE.sentence(),
        phone=FAKE.phone_number(),
        city=FAKE.city(),
        country=FAKE.country_code(),
        timezone="Europe/Amsterdam",
        email=FAKE.ascii_email(),
        source_url=FAKE.url(),
        url=FAKE.url(),
    )


@pytest.fixture
def valid_event(valid_venue: Venue) -> Event:
    return Event(
        url=FAKE.url(),
        description=FAKE.sentence(),
        title=FAKE.sentence(),
        source=valid_venue.source_url,
        date_published=FAKE.past_date(start_date="-1d", tzinfo=pytz.timezone("Europe/Amsterdam")),
        image_url=FAKE.uri(),
        venue=valid_venue,
        when=FAKE.date_time_this_year(before_now=False, after_now=True, tzinfo=pytz.timezone("Europe/Amsterdam")),
    )


@pytest.fixture
def valid_user_profile() -> UserProfile:
    return UserProfile(
        email=FAKE.ascii_email(), given_name=FAKE.first_name(), family_name=FAKE.last_name(), avatar_url=FAKE.uri()
    )


@pytest.fixture
async def client_session():
    timeout = ClientTimeout(40)
    a_client_session = ClientSession(timeout=timeout)
    yield a_client_session
    await a_client_session.close()
