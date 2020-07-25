from flask import Flask

from core_lib.api.cron import CRON_ROUTES
from core_lib.api.maintenance import MAINTENANCE_ROUTES
from core_lib.core.app_config import AppConfig

APP = Flask(__name__, static_folder="static/build/static", template_folder="static/build")

APP.register_blueprint(CRON_ROUTES)
APP.register_blueprint(MAINTENANCE_ROUTES)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=AppConfig.get_port(), debug=False)
