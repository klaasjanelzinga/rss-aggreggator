from typing import Any, Dict

from flask import Blueprint, jsonify

from app import application_data
from app.core.venue.venue import Venue

VENUE_API_ROUTES = Blueprint('venues', __name__, template_folder='templates')


@VENUE_API_ROUTES.route('/api/venues', methods=['GET'])
def fetch_events() -> Any:
    venues = application_data.venue_repository.fetch_all()
    return jsonify({
        'venues': [_transform(venue) for venue in venues]
    })


def _transform(venue: Venue) -> Dict:
    return {
        'venue_id': venue.venue_id,
        'city': venue.city,
        'country': venue.country,
        'email': venue.email,
        'name': venue.name,
        'phone': venue.phone,
        'source_url': venue.source_url,
        'lastFetchedDate': venue.convert_utc_to_venue_timezone(venue.last_fetched_date).isoformat(),
        'url': venue.url
    }
