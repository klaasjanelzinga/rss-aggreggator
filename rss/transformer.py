from core.item import Item
from rss.item import RSSItem


class Transformer:

    @staticmethod
    def item_to_rss(item: Item) -> RSSItem:
        return RSSItem(title=item.title,
                       link=item.url,
                       description=item.description,
                       author=item.source,
                       guid=item.url,
                       source=item.source)

