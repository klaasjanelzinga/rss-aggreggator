from typing import Any

from flask import Blueprint, Response

MAINTENANCE_ROUTES = Blueprint("maintenance", __name__, template_folder="templates")


@MAINTENANCE_ROUTES.route("/maintenance/ping")
def maintenance_ping() -> Any:
    return Response(status=200)
