from typing import Any

from flask import Flask, render_template, send_from_directory

from app.api.api import EVENT_API_ROUTES
from app.api.maintenance import MAINTENANCE_ROUTES
from app.api.user_api import USER_ROUTES
from app.api.venue import VENUE_API_ROUTES
from app.rss.rss_api import RSS_ROUTES

# set to react specific build artifacts, NOTE, only localhost, gae -> app.yaml
# pylint: disable=C0103
app = Flask(__name__, static_folder="static/build/static", template_folder="static/build")

app.register_blueprint(EVENT_API_ROUTES)
app.register_blueprint(MAINTENANCE_ROUTES)
app.register_blueprint(RSS_ROUTES)
app.register_blueprint(USER_ROUTES)
app.register_blueprint(VENUE_API_ROUTES)


@app.route("/")
def hello() -> Any:
    return render_template("index.html")


@app.route("/channel-image.png")
def send_channel_image() -> Any:
    return send_from_directory("static/build", "channel-image.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
# [END gae_python37_app]
