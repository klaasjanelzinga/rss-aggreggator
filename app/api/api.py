from typing import Any

from flask import Blueprint, jsonify, request

from app import application_data
from app.application_data import event_repository
from app.core.event import Event
from app.core.event_entity_transformer import EventEntityTransformer

API_ROUTES = Blueprint('api', __name__, template_folder='templates')

EVENT_ENTITY_TRANSFORMER = EventEntityTransformer(venue_repository=application_data.venue_repository)


# original runs in 100ms
@API_ROUTES.route('/api/events', methods=['GET'])
def fetch_events() -> Any:
    # if not AppConfig.is_running_in_gae():
    #     with open('tests/sample-api-events.json') as f:
    #         ob = json.load(f)
    #         logging.warning('Returning stubbed event data!')
    #         return jsonify(ob)
    #
    fetch_offset = request.args.get('fetch_offset')
    cursor = bytes(fetch_offset, 'utf-8') if fetch_offset is not None else None

    query_result = event_repository.fetch_items(cursor=cursor, limit=25)
    events = [transform(EVENT_ENTITY_TRANSFORMER.to_event(item)) for item in query_result.items]

    return jsonify({
        'events': events,
        'fetch_offset': query_result.token.decode('utf-8')
    })


@API_ROUTES.route('/api/search', methods=['GET'])
def search_events() -> Any:
    term = request.args.get('term')
    fetch_offset = request.args.get('fetch_offset')
    cursor = bytes(fetch_offset, 'utf-8') if fetch_offset is not None else None
    if term is None:
        return fetch_events()
    query_result = event_repository.search(term=term, cursor=cursor, limit=25)
    events = [transform(EVENT_ENTITY_TRANSFORMER.to_event(item)) for item in query_result.items]

    return jsonify({
        'events': events,
        'fetch_offset': query_result.token.decode('utf-8')
    })


def transform(event: Event) -> dict:
    venue = event.venue
    return {
        'id': event.event_id,
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
