from flask import Flask, Response, render_template, send_from_directory

from api.api import api_routes
from api.maintenance import maintenance
from application_data import event_repository, venue_repository
from core.app_config import AppConfig
from rss.channel import RSSChannel
from rss.transformer import Transformer
from venues.oost_groningen.oost_groningen_processor import OostGroningenProcessor
from venues.simplon_groningen.simplon_processor import SimplonProcessor
from venues.spot.spot_processor import SpotProcessor
from venues.tivoli_utrecht.tivoli_processor import TivoliProcessor
from venues.vera_groningen.vera_processor import VeraProcessor

# set to react specific build artifacts, NOTE, only localhost, gae -> app.yaml
app = Flask(__name__, static_folder='static/build/static', template_folder='static/build')

# sync stores at start of app and register venues
processors = [SpotProcessor(event_repository),
              VeraProcessor(event_repository),
              OostGroningenProcessor(event_repository),
              SimplonProcessor(event_repository),
              TivoliProcessor(event_repository)]
[processor.sync_stores() for processor in processors if not AppConfig.is_running_in_gae()]
[processor.register_venue_at(venue_repository) for processor in processors]

app.register_blueprint(api_routes)
app.register_blueprint(maintenance)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/channel-image.png')
def send_channel_image():
    return send_from_directory('static/build', 'channel-image.png')


@app.route('/events.xml')
def fetch_rss():
    items = [Transformer.item_to_rss(venue_repository, item) for item in event_repository.fetch_items()[0]]
    channel = RSSChannel(items)
    return Response(channel.to_xml(), mimetype='application/rss+xml')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
