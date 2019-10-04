from typing import Any, Generator

from flask import Blueprint, Response

from app.application_data import event_repository, event_entity_transformer
from app.rss.channel import RSSChannel
from app.rss.transformer import Transformer

RSS_ROUTES = Blueprint("rss", __name__, template_folder="templates")


@RSS_ROUTES.route("/events.xml")
def fetch_rss() -> Any:
    def generate() -> Generator:
        rss_channel = RSSChannel()
        pre_amble = rss_channel.generate_pre_amble()
        yield pre_amble.replace("</rss>", "").replace("</channel>", "").encode("UTF-8")
        for event in [event_entity_transformer.to_event(event) for event in event_repository.fetch_all_items()]:
            yield Transformer.item_to_rss(event).as_node()
        yield rss_channel.generate_post_amble()

    return Response(generate(), mimetype="text/xml")
