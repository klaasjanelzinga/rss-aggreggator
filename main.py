import logging
from datetime import datetime, timedelta

from flask import Flask, Response, request
from google.cloud import datastore

from core.app_config import AppConfig
from core.event_repository import EventRepository
from core.venue_repository import VenueRepository
from rss.channel import RSSChannel
from rss.transformer import Transformer
from spot.processor import SpotProcessor

logging.basicConfig(level=logging.INFO)


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

datastore_client = datastore.Client()
event_repository = EventRepository(datastore_client)
venue_repository = VenueRepository()

# sync stores at start of app and register venues
spot_processor = SpotProcessor(event_repository)
spot_processor.sync_stores()
spot_processor.register_venue_at(venue_repository)


@app.route('/')
def hello():
    return 'Hello World! App soon to arrive.'


@app.route('/maintenance/fetch-data')
def maintenance_fetch_data():
    if AppConfig.is_web_request_allowed(request):
        venue_id = request.args.get('venue_id')
        venue_repository.sync_stores_for_venue(venue_id)
        return Response()
    return Response(status=400)


@app.route('/maintenance/cleanup')
def maintenance_clean_up():
    if AppConfig.is_web_request_allowed(request):
        number_cleaned = event_repository.clean_items_before(datetime.now() - timedelta(days=3))
        logging.info(f'Number of items cleaned {number_cleaned}')
        return Response(status=200)
    return Response(status=400)


@app.route('/events.xml')
def fetch_rss():
    items = [Transformer.item_to_rss(venue_repository, item) for item in event_repository.fetch_items()]
    channel = RSSChannel(items)
    return Response(channel.to_xml(), mimetype='application/rss+xml')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
