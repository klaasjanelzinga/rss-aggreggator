from datetime import datetime, timedelta
import logging
from typing import Any

from flask import Blueprint, Response, request

from app import application_data
from app.application_data import OC_TRACER, event_repository
from app.core.app_config import AppConfig
from app.application_data import venue_repository

MAINTENANCE_ROUTES = Blueprint("maintenance", __name__, template_folder="templates")


@MAINTENANCE_ROUTES.route("/maintenance/fetch-data")
def maintenance_fetch_data() -> Any:
    if AppConfig.is_web_request_allowed(request):
        with OC_TRACER.span("fetch_data"):
            application_data.sync_venues()
            return Response(status=200)
    return Response(status=400)


@MAINTENANCE_ROUTES.route("/maintenance/fetch-integration-test-data")
def maintenance_fetch_integration_test_data() -> Any:
    if AppConfig.is_web_request_allowed(request):
        with OC_TRACER.span("fetch_integration_test_data"):
            application_data.sync_integration_test_venues()
            return Response(status=200)
    return Response(status=400)


@MAINTENANCE_ROUTES.route("/maintenance/fetch-all-data")
def maintenance_fetch_all_data() -> Any:
    if AppConfig.is_web_request_allowed(request):
        with OC_TRACER.span("fetch_all_data"):
            application_data.sync_all_venues()
            return Response(status=200)
    return Response(status=400)


@MAINTENANCE_ROUTES.route("/maintenance/cleanup")
def maintenance_clean_up() -> Any:
    if AppConfig.is_web_request_allowed(request):
        with OC_TRACER.span("maintenance_cleanup"):
            number_cleaned = event_repository.clean_items_before(datetime.now() - timedelta(hours=2))
            logging.getLogger(__name__).info("Number of items cleaned %d", number_cleaned)
            return Response(status=200)
    return Response(status=400)


@MAINTENANCE_ROUTES.route("/maintenance/cleanup-all")
def maintenance_clean_up_all() -> Any:
    if AppConfig.is_web_request_allowed(request):
        with OC_TRACER.span("maintenance_cleanup_all"):
            number_cleaned = event_repository.clean_items_before(datetime(9999, 1, 1, 1, 1, 1))
            for venue in venue_repository.fetch_all():
                venue.last_fetched_date = datetime.min
                venue_repository.upsert(venue)
            logging.getLogger(__name__).info("Number of items cleaned %d", number_cleaned)
            return Response(status=200)
    return Response(status=400)


@MAINTENANCE_ROUTES.route("/maintenance/ping")
def maintenance_ping() -> Any:
    return Response(status=200)
