from unittest.mock import Mock

import pytest
import pytz
from aiohttp import ClientSession, ClientTimeout
from faker import Faker

from app.core.event.event import Event
from app.core.event.event_repository import EventRepository
from app.core.user.user_profile import UserProfile
from app.core.venue.venue import Venue
from app.core.venue.venue_repository import VenueRepository
from app.venues.hedon_zwolle.hedon_processor import HedonProcessor
from app.venues.melkweg_amsterdam.melkweg_processor import MelkwegProcessor
from app.venues.neushoorn_leeuwarden.neushoorn_processor import NeushoornProcessor
from app.venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor
from app.venues.paradiso_amsterdam.paradiso_processor import ParadisoProcessor
from app.venues.simplon_groningen.simplon_processor import SimplonProcessor
from app.venues.spot.spot_processor import SpotProcessor
from app.venues.t013_tilburg.t013_processor import T013Processor
from app.venues.tivoli_utrecht.tivoli_processor import TivoliProcessor
from app.venues.vera_groningen.vera_processor import VeraProcessor

FAKE = Faker()


@pytest.fixture
def mock_venue_repository() -> VenueRepository:
    return Mock(spec=VenueRepository)


@pytest.fixture
def mock_event_repository() -> EventRepository:
    return Mock(spec=EventRepository)


@pytest.fixture
def hedon_processor(mock_event_repository, mock_venue_repository) -> HedonProcessor:
    return HedonProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def melkweg_processor(mock_event_repository, mock_venue_repository) -> MelkwegProcessor:
    return MelkwegProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def neushoorn_processor(mock_event_repository, mock_venue_repository) -> NeushoornProcessor:
    return NeushoornProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def oost_processor(mock_event_repository, mock_venue_repository) -> OostGroningenProcessor:
    return OostGroningenProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def paradiso_processor(mock_event_repository, mock_venue_repository) -> ParadisoProcessor:
    return ParadisoProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def simplon_processor(mock_event_repository, mock_venue_repository) -> SimplonProcessor:
    return SimplonProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def spot_processor(mock_event_repository, mock_venue_repository) -> SpotProcessor:
    return SpotProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def t013_processor(mock_event_repository, mock_venue_repository) -> T013Processor:
    return T013Processor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def tivoli_processor(mock_event_repository, mock_venue_repository) -> TivoliProcessor:
    return TivoliProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


@pytest.fixture
def vera_processor(mock_event_repository, mock_venue_repository) -> VeraProcessor:
    return VeraProcessor(
        event_repository=mock_event_repository,
        venue_repository=mock_venue_repository,
    )


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
