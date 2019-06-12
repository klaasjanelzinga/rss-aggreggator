from flask import Flask, render_template, send_from_directory

from app.api.api import api_routes
from app.api.maintenance import maintenance
from app.application_data import processors
from app.core.app_config import AppConfig
from app.rss.rss_api import rss_routes

# set to react specific build artifacts, NOTE, only localhost, gae -> app.yaml
app = Flask(__name__, static_folder='static/build/static', template_folder='static/build')

# sync stores at start of app
[processor.sync_stores() for processor in processors if not AppConfig.is_running_in_gae()]

app.register_blueprint(api_routes)
app.register_blueprint(maintenance)
app.register_blueprint(rss_routes)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/channel-image.png')
def send_channel_image():
    return send_from_directory('static/build', 'channel-image.png')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
