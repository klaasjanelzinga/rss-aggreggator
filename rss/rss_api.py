from flask import Blueprint, Response

from application_data import event_repository, event_entity_transformer
from rss.channel import RSSChannel
from rss.transformer import Transformer

rss_routes = Blueprint('rss', __name__, template_folder='templates')


@rss_routes.route('/events.xml')
def fetch_rss():
    def generate():
        rss_channel = RSSChannel()
        pre_amble = rss_channel.generate_pre_amble()
        yield pre_amble.replace('</rss>', '').replace('</channel>', '').encode('UTF-8')
        for q in event_repository.fetch_all_items():
            event = event_entity_transformer.to_event(q)
            yield Transformer.item_to_rss(event).as_node()
        yield rss_channel.generate_post_amble()

    return Response(generate(), mimetype='text/xml')
