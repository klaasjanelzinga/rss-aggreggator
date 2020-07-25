from hamcrest import assert_that, equal_to, matches_regexp

from core_lib.rss.transformer import Transformer
from core_lib.core.event.event import Event


def test_as_xml(valid_event: Event):
    event = valid_event
    rss_item = Transformer().item_to_rss(event)
    assert_that(rss_item.title, equal_to(f"{valid_event.title} [{valid_event.venue.short_name}]"))
    assert_that(rss_item.author, equal_to(valid_event.source))
    assert_that(rss_item.guid, equal_to(valid_event.url))
    assert_that(rss_item.link, equal_to(valid_event.url))
    description = rss_item.description
    assert_that(description, matches_regexp(f"<p>{valid_event.description}</p>"))
    assert_that(
        description,
        matches_regexp(
            f'Where: <a href="{valid_event.venue.url}">{valid_event.venue.name} .{valid_event.venue.city}, {valid_event.venue.country}.</a></p>'
        ),
    )
    assert_that(description, matches_regexp("<p>When: \\d{4}-\\d\\d-\\d\\d \\d\\d:\\d\\d -"))
