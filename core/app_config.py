import logging
import os
from datetime import datetime

from flask import request
from pytz import timezone


class AppConfig:

    @staticmethod
    def is_running_in_gae() -> bool:
        return 'GAE_ENV' in os.environ

    @staticmethod
    def is_web_request_allowed(request: request) -> bool:
        if not AppConfig.is_running_in_gae():
            logging.warning('Allowing request since not running in gae')
            return True
        if 'X-Appengine-Cron' in request.headers:
            return True
        logging.warning('Header not set on web request. Request denied')
        return False

    @staticmethod
    def datetime_utc_to_amsterdam(utc: datetime):
        amsterdam = timezone('Europe/Amsterdam')
        return utc.astimezone(amsterdam)
