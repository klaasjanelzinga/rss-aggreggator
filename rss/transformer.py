from core.event import Event
from core.venue_repository import VenueRepository
from rss.rss_item import RSSItem


class Transformer:

    @staticmethod
    def item_to_rss(venue_repository: VenueRepository, item: Event) -> RSSItem:
        venue = venue_repository.get_venue_for(item.venue_id)
        when = item.when.strftime('%Y-%m-%d %H:%M')
        description = \
            f'''<![CDATA[<html><body>
            <p>{item.description}</p>
            <img src="{item.image_url}" alt="image for event" width=300 height=160/>
            <p>When: {when} - 
               Where: <a href="{venue.url}">{venue.name} ({venue.city}, {venue.country})</a></p>
            </body></html>]]>'''
        return RSSItem(title=item.title,
                       link=item.url,
                       description=description,
                       author=item.source,
                       guid=item.url,
                       source=item.source)
