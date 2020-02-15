from flask import Flask

from app.api.api import EVENT_API_ROUTES
from app.api.maintenance import MAINTENANCE_ROUTES
from app.api.user_api import USER_ROUTES
from app.api.venue import VENUE_API_ROUTES
from app.core.app_config import AppConfig
from app.rss.rss_api import RSS_ROUTES

APP = Flask(__name__, static_folder="static/build/static", template_folder="static/build")

APP.register_blueprint(EVENT_API_ROUTES)
APP.register_blueprint(MAINTENANCE_ROUTES)
APP.register_blueprint(RSS_ROUTES)
APP.register_blueprint(USER_ROUTES)
APP.register_blueprint(VENUE_API_ROUTES)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=AppConfig.get_port(), debug=False)
