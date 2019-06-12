from flask import Blueprint, jsonify, request

from app.application_data import event_repository
from app.core.event import Event

api_routes = Blueprint('api', __name__, template_folder='templates')


@api_routes.route('/api/events', methods=['GET'])
def fetch_events():
    fetch_offset = request.args.get('fetch_offset')
    cursor = bytes(fetch_offset, 'utf-8') if fetch_offset is not None else None

    events, new_fetch_offset = event_repository.fetch_items(cursor=cursor, limit=25)
    sorted(events, key=lambda event: event.when)
    return jsonify({
        'events': [transform(item) for item in events],
        'fetch_offset': new_fetch_offset.decode('utf-8')
    })


@api_routes.route('/api/search', methods=['GET'])
def search_events():
    term = request.args.get('term')
    fetch_offset = request.args.get('fetch_offset')
    cursor = bytes(fetch_offset, 'utf-8') if fetch_offset is not None else None
    if term is None:
        return fetch_events()
    events, new_fetch_offset = event_repository.search(term=term, cursor=cursor, limit=25)
    return jsonify({
        'events': [transform(item) for item in events],
        'fetch_offset': new_fetch_offset.decode('utf-8')
    })


def transform(event: Event) -> dict:
    venue = event.venue
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