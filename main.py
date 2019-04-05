import logging
import os

from core.item_store import ItemStore
from rss.transformer import Transformer
from rss.channel_factory import ChannelFactory
from spot.processor import SpotProcessor

logging.basicConfig(level=logging.INFO)

from flask import Flask, Response

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
  pass
  # Production
else:
  pass


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/aggregated-events.xml')
def fetch_rss():
    items = [Transformer.item_to_rss(item) for item in ItemStore().fetch_items()]
    channel = ChannelFactory.create_default_channel(items)
    return Response(channel.as_xml(), mimetype='text/xml')


@app.route('/dummy-events.xml')
def fetch_dummy_rss():
    spot = SpotProcessor().dummy_items()
    rss_items = [Transformer.item_to_rss(item) for item in spot.items]
    channel = ChannelFactory.create_default_channel(rss_items)
    return Response(channel.as_xml(), mimetype='text/xml')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
