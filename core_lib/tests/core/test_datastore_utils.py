from hamcrest import has_items
from hamcrest.core import assert_that

from core_lib.core.models import split_term


def test_search_terms():
    term = "heel erg leuke metal band in vera-groningen"
    search_terms = split_term(term)
    assert_that(search_terms, has_items("heel", "vera", "groningen"))
