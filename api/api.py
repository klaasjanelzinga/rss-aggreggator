from flask import Blueprint, jsonify, Response

from application_data import venue_repository, event_repository
from core.event import Event

api_routes = Blueprint('api', __name__, template_folder='templates')


@api_routes.route('/api/events', methods=['OPTIONS'])
def options_maintenance_fetch_data():
    return Response(status=200)


@api_routes.route('/api/events', methods=['GET'])
def maintenance_fetch_data():
    events = event_repository.fetch_items()
    sorted(events, key=lambda event: event.when)
    return jsonify([transform(item) for item in event_repository.fetch_items()])
    # if AppConfig.is_running_in_gae():
    # else:
    #     with open('tests/samples/api/events.json') as f:
    #         return Response(''.join(f.readlines()), 'application/json')


def transform(event: Event) -> dict:
    venue = venue_repository.get_venue_for(event.venue_id)
    return {
        'id': event.id,
        'url': event.url,
        'title': event.title,
        'description': event.description,
        'image_url': event.image_url,
        'when': venue.convert_utc_to_venue_timezone(event.when).isoformat(),
        'venue': {
            'id': venue.venue_id,
            'name': venue.name,
            'city': venue.city
        }
    }
