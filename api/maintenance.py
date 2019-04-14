import logging
from datetime import timedelta, datetime

from flask import Blueprint, request, Response

from application_data import venue_repository, event_repository
from core.app_config import AppConfig

maintenance = Blueprint('maintenance', __name__, template_folder='templates')


@maintenance.route('/maintenance/fetch-data')
def maintenance_fetch_data():
    if AppConfig.is_web_request_allowed(request):
        venue_id = request.args.get('venue_id')
        if venue_id is None or not venue_repository.is_registered(venue_id):
            return Response(status=404)
        venue_repository.sync_stores_for_venue(venue_id)
        return Response()
    return Response(status=400)


@maintenance.route('/maintenance/cleanup')
def maintenance_clean_up():
    if AppConfig.is_web_request_allowed(request):
        number_cleaned = event_repository.clean_items_before(datetime.now() - timedelta(days=3))
        logging.info(f'Number of items cleaned {number_cleaned}')
        return Response(status=200)
    return Response(status=400)



