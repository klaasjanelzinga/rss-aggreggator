from app.core.event import Event
from app.rss.rss_item import RSSItem


class Transformer:

    @staticmethod
    def item_to_rss(item: Event) -> RSSItem:
        venue = item.venue
        when = venue.convert_utc_to_venue_timezone(item.when).strftime('%Y-%m-%d %H:%M')
        description = \
            f'''<html><body>
            <p>{item.description}</p>
            <img src="{item.image_url}" alt="image for event" width=300 height=160/>
            <p>When: {when} -
               Where: <a href="{venue.url}">{venue.name} ({venue.city}, {venue.country})</a></p>
            </body></html>'''
        return RSSItem(title=item.title,
                       link=item.url,
                       description=description,
                       author=item.source,
                       guid=item.url,
                       source=item.source)
