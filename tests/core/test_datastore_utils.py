from hamcrest import has_items
from hamcrest.core import assert_that

from app.core.datastore_utils import DatastoreUtils


def test_search_terms():
    term = "heel erg leuke metal band in vera-groningen"
    search_terms = DatastoreUtils.split_term(term)
    assert_that(search_terms, has_items("heel", "vera", "groningen"))
