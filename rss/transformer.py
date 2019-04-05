from core.event import Event
from rss.rss_item import RSSItem


class Transformer:

    @staticmethod
    def item_to_rss(item: Event) -> RSSItem:
        when = item.when.strftime('%Y-%m-%d %H:%M')
        description = \
            f'''<![CDATA[<html><body>
            <p>{item.description}</p>
            <img src="{item.image_url}" alt="image for event" width=300 height=160/>
            <p>When: {when} - Where: <a href="{item.source}">{item.venue_id}</a></p>
            </body></html>]]>'''
        return RSSItem(title=item.title,
                       link=item.url,
                       description=description,
                       author=item.source,
                       guid=item.url,
                       source=item.source)
