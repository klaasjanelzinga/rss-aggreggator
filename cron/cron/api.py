import logging
from datetime import datetime, timedelta
from typing import Any

from flask import Blueprint, Response

from core_lib import application_data
from core_lib.application_data import event_repository, venue_repository

MAINTENANCE_ROUTES = Blueprint("maintenance", __name__, template_folder="templates")
CRON_ROUTES = Blueprint("cron", __name__, template_folder="templates")


@MAINTENANCE_ROUTES.route("/maintenance/ping")
def maintenance_ping() -> Any:
    return Response(status=200)


@CRON_ROUTES.route("/cron/fetch-data")
def maintenance_fetch_data() -> Any:
    application_data.sync_venues()
    return Response(status=200)


@CRON_ROUTES.route("/cron/fetch-integration-test-data")
def maintenance_fetch_integration_test_data() -> Any:
    application_data.sync_integration_test_venues()
    return Response(status=200)


@CRON_ROUTES.route("/cron/fetch-all-data")
def maintenance_fetch_all_data() -> Any:
    application_data.sync_all_venues()
    return Response(status=200)


@CRON_ROUTES.route("/cron/cleanup")
def maintenance_clean_up() -> Any:
    number_cleaned = event_repository.clean_items_before(datetime.now() - timedelta(hours=2))
    logging.getLogger(__name__).info("Number of items cleaned %d", number_cleaned)
    return Response(status=200)


@CRON_ROUTES.route("/cron/cleanup-all")
def maintenance_clean_up_all() -> Any:
    number_cleaned = event_repository.clean_items_before(datetime(9999, 1, 1, 1, 1, 1))
    for venue in venue_repository.fetch_all():
        venue.last_fetched_date = datetime.min
        venue_repository.upsert(venue)
    logging.getLogger(__name__).info("Number of items cleaned %d", number_cleaned)
    return Response(status=200)
