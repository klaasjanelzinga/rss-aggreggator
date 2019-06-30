from typing import Any

from flask import Flask, render_template, send_from_directory

from app.api.api import API_ROUTES
from app.api.maintenance import MAINTENANCE_ROUTES
from app.application_data import processors
from app.core.app_config import AppConfig
from app.rss.rss_api import RSS_ROUTES

# set to react specific build artifacts, NOTE, only localhost, gae -> app.yaml
# pylint: disable=C0103
app = Flask(__name__, static_folder='static/build/static', template_folder='static/build')

# sync stores at start of app
# pylint: disable=W0106
[processor.sync_stores() for processor in processors if not AppConfig.is_running_in_gae()]

app.register_blueprint(API_ROUTES)
app.register_blueprint(MAINTENANCE_ROUTES)
app.register_blueprint(RSS_ROUTES)


@app.route('/')
def hello() -> Any:
    return render_template('index.html')


@app.route('/channel-image.png')
def send_channel_image() -> Any:
    return send_from_directory('static/build', 'channel-image.png')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
