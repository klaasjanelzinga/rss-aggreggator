from flask import Blueprint, Response
from rx.operators import map

from application_data import event_repository, venue_repository
from rss.channel import RSSChannel
from rss.transformer import Transformer

rss_routes = Blueprint('rss', __name__, template_folder='templates')


@rss_routes.route('/events.xml')
def fetch_rss():
    venue_filtered_items = [event for event in event_repository.fetch_items()[0]
                            if venue_repository.is_registered(event.venue.venue_id)]
    rss_items = [Transformer.item_to_rss(item) for item in venue_filtered_items]
    channel = RSSChannel(rss_items)
    return Response(channel.to_xml(), mimetype='application/rss+xml')
