from core.event import Event
from rss.rss_item import RSSItem


class Transformer:

    @staticmethod
    def item_to_rss(item: Event) -> RSSItem:
        return RSSItem(title=item.title,
                       link=item.url,
                       description=item.description,
                       author=item.source,
                       guid=item.url,
                       source=item.source)

