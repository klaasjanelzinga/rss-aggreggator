from flask import Flask

from api.api import (
    EVENT_API_ROUTES,
    USER_ROUTES,
    VENUE_API_ROUTES,
    MAINTENANCE_ROUTES,
    RSS_ROUTES,
)
from core_lib.core.app_config import AppConfig

APP = Flask(
    __name__, static_folder="static/build/static", template_folder="static/build"
)

APP.register_blueprint(EVENT_API_ROUTES)
APP.register_blueprint(MAINTENANCE_ROUTES)
APP.register_blueprint(RSS_ROUTES)
APP.register_blueprint(USER_ROUTES)
APP.register_blueprint(VENUE_API_ROUTES)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=AppConfig.get_port(), debug=False)
