from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to

from core_lib.core.models import Venue
from core_lib.core.repositories import VenueEntityTransformer


def test_to_entity(valid_venue: Venue):
    transformer = VenueEntityTransformer()
    entity = transformer.to_entity(valid_venue)
    assert_that(entity["name"], equal_to(valid_venue.name))
    assert_that(entity["short_name"], equal_to(valid_venue.short_name))
    assert_that(entity["timezone"], equal_to(valid_venue.timezone))
    assert_that(entity["venue_id"], equal_to(valid_venue.venue_id))
    assert_that(entity["phone"], equal_to(valid_venue.phone))
    assert_that(entity["email"], equal_to(valid_venue.email))
    assert_that(entity["city"], equal_to(valid_venue.city))
    assert_that(entity["country"], equal_to(valid_venue.country))
    assert_that(entity["url"], equal_to(valid_venue.url))
    assert_that(entity["last_fetched_date"], equal_to(valid_venue.last_fetched_date))
    assert_that(entity["search_terms"], equal_to(valid_venue.search_terms))
    assert_that(len(entity), equal_to(12))


def test_from_entity(valid_venue: Venue):
    transformer = VenueEntityTransformer()
    entity = transformer.to_entity(valid_venue)
    venue = transformer.to_venue(entity)
    assert_that(venue.name, equal_to(valid_venue.name))
    assert_that(venue.short_name, equal_to(valid_venue.short_name))
    assert_that(venue.timezone, equal_to(valid_venue.timezone))
    assert_that(venue.venue_id, equal_to(valid_venue.venue_id))
    assert_that(venue.phone, equal_to(valid_venue.phone))
    assert_that(venue.email, equal_to(valid_venue.email))
    assert_that(venue.city, equal_to(valid_venue.city))
    assert_that(venue.country, equal_to(valid_venue.country))
    assert_that(venue.url, equal_to(valid_venue.url))
    assert_that(venue.last_fetched_date, equal_to(valid_venue.last_fetched_date))
    assert_that(venue.search_terms, equal_to(valid_venue.search_terms))
