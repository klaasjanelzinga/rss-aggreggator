import logging
from datetime import timedelta, datetime
from typing import Any

from flask import Blueprint, request, Response

from app.application_data import venue_repository, event_repository, processors_map
from app.core.app_config import AppConfig

MAINTENANCE_ROUTES = Blueprint('maintenance', __name__, template_folder='templates')


@MAINTENANCE_ROUTES.route('/maintenance/fetch-data')
def maintenance_fetch_data() -> Any:
    if AppConfig.is_web_request_allowed(request):
        venue_id = request.args.get('venue_id')
        if venue_id is None or not venue_repository.is_registered(venue_id):
            return Response(status=404)
        processors_map[venue_id].sync_stores()
        return Response()
    return Response(status=400)


@MAINTENANCE_ROUTES.route('/maintenance/cleanup')
def maintenance_clean_up() -> Any:
    if AppConfig.is_web_request_allowed(request):
        number_cleaned = event_repository.clean_items_before(datetime.now() - timedelta(hours=2))
        logging.getLogger(__name__).info('Number of items cleaned %d', number_cleaned)
        return Response(status=200)
    return Response(status=400)


@MAINTENANCE_ROUTES.route('/maintenance/ping')
def maintenance_ping() -> Any:
    return Response(status=200)
