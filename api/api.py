import base64

from flask import Blueprint, jsonify, Response, request

from application_data import venue_repository, event_repository
from core.event import Event

api_routes = Blueprint('api', __name__, template_folder='templates')


@api_routes.route('/api/events', methods=['GET'])
def fetch_events():
    fetch_offset = request.args.get('fetch_offset')
    cursor = bytes(fetch_offset, 'utf-8') if fetch_offset is not None else None

    events, new_fetch_offset = event_repository.fetch_items(cursor=cursor, limit=5)
    sorted(events, key=lambda event: event.when)
    return jsonify({
        'events': [transform(item) for item in events],
        'fetch_offset': new_fetch_offset.decode('utf-8')
    })
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
