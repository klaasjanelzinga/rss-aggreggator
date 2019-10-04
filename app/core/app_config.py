import logging
import os

from flask import Request


class AppConfig:
    @staticmethod
    def is_running_in_gae() -> bool:
        return "GAE_ENV" in os.environ or "DUMMY_GAE_LOCAL" in os.environ

    @staticmethod
    def is_web_request_allowed(req: Request) -> bool:
        logger = logging.getLogger(__name__)
        if not AppConfig.is_running_in_gae():
            logger.warning("Allowing request since not running in gae")
            return True
        if "X-Appengine-Cron" in req.headers:
            return True
        logger.warning("Header not set on web request. Request denied")
        return False
