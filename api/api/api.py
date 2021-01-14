from datetime import date, timedelta
from typing import Any, Dict, Generator

from flask import Blueprint, jsonify, request, Response
from flask_cors import cross_origin

from core_lib.application_data import repositories, event_entity_transformer
from core_lib.core.app_config import AppConfig
from core_lib.core.models import Event, Venue
from core_lib.core.repositories import EventEntityTransformer
from core_lib.core.rss import RSSChannel, Transformer
from core_lib.core.token_verifier import TokenVerifier
from core_lib.core.user_profile import UserProfile

EVENT_API_ROUTES = Blueprint("events", __name__, template_folder="templates")
EVENT_ENTITY_TRANSFORMER = EventEntityTransformer(
    venue_repository=repositories.venue_repository
)
VENUE_API_ROUTES = Blueprint("venues", __name__, template_folder="templates")
USER_ROUTES = Blueprint("user", __name__, template_folder="templates")
MAINTENANCE_ROUTES = Blueprint("maintenance", __name__, template_folder="templates")
RSS_ROUTES = Blueprint("rss", __name__, template_folder="templates")


@MAINTENANCE_ROUTES.route("/maintenance/ping")
def maintenance_ping() -> Any:
    return Response(status=200)


@EVENT_API_ROUTES.route("/api/events", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_events() -> Any:
    # if not AppConfig.is_running_in_gae():
    #     with open('tests/sample-api-events.json') as f:
    #         ob = json.load(f)
    #         logging.warning('Returning stubbed event data!')
    #         return jsonify(ob)
    fetch_offset = request.args.get("fetch_offset")
    cursor = bytes(fetch_offset, "utf-8") if fetch_offset is not None else None

    query_result = repositories.event_repository.fetch_items(cursor=cursor, limit=25)
    events = [
        transform(EVENT_ENTITY_TRANSFORMER.to_event(item))
        for item in query_result.items
    ]

    return jsonify(
        {"events": events, "fetch_offset": query_result.token.decode("utf-8")}
    )


@EVENT_API_ROUTES.route("/api/events/today", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_today_events() -> Any:
    query_result = repositories.event_repository.fetch_items_on(when=date.today())
    events = [
        transform(EVENT_ENTITY_TRANSFORMER.to_event(item))
        for item in query_result.items
    ]
    return jsonify(
        {"events": events, "fetch_offset": query_result.token.decode("utf-8")}
    )


@EVENT_API_ROUTES.route("/api/events/tomorrow", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_tomorrow_events() -> Any:
    query_result = repositories.event_repository.fetch_items_on(
        when=date.today() + timedelta(days=1)
    )
    events = [
        transform(EVENT_ENTITY_TRANSFORMER.to_event(item))
        for item in query_result.items
    ]
    return jsonify(
        {"events": events, "fetch_offset": query_result.token.decode("utf-8")}
    )


@EVENT_API_ROUTES.route("/api/events/day-after-tomorrow", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_day_after_tomorrow_events() -> Any:
    query_result = repositories.event_repository.fetch_items_on(
        when=date.today() + timedelta(days=2)
    )
    events = [
        transform(EVENT_ENTITY_TRANSFORMER.to_event(item))
        for item in query_result.items
    ]
    return jsonify(
        {"events": events, "fetch_offset": query_result.token.decode("utf-8")}
    )


@EVENT_API_ROUTES.route("/api/search", methods=["GET"])
@cross_origin(**AppConfig.cors())
def search_events() -> Any:
    term = request.args.get("term")
    fetch_offset = request.args.get("fetch_offset")
    cursor = bytes(fetch_offset, "utf-8") if fetch_offset is not None else None
    if term is None:
        return fetch_events()
    query_result = repositories.event_repository.search(
        term=term, cursor=cursor, limit=25
    )
    events = [
        transform(EVENT_ENTITY_TRANSFORMER.to_event(item))
        for item in query_result.items
    ]

    return jsonify(
        {"events": events, "fetch_offset": query_result.token.decode("utf-8")}
    )


def transform(event: Event) -> dict:
    venue = event.venue
    return {
        "id": event.event_id,
        "url": event.url,
        "title": event.title,
        "description": event.description,
        "image_url": event.image_url,
        "when": event.when.isoformat(),
        "venue": {"id": venue.venue_id, "name": venue.name, "city": venue.city},
    }


@USER_ROUTES.route("/api/user/signup", methods=["POST"])
@cross_origin(**AppConfig.cors())
def login_user() -> Any:

    user_profile_token = TokenVerifier.verify_for_headers(request.headers)
    if not user_profile_token:
        return Response(status=404)

    user_profile_in_request = transform_to_user_profile(request.json)
    user_profile = repositories.user_profile_repository.fetch_user_by_email(
        user_profile_in_request.email
    )
    if user_profile:
        return jsonify(transform_to_json(user_profile))

    user_profile = repositories.user_profile_repository.insert(user_profile_in_request)
    return jsonify(transform_to_json(user_profile)), 201


@USER_ROUTES.route("/api/user/profile", methods=["POST"])
@cross_origin(**AppConfig.cors())
def update_user() -> Any:
    user_profile_token = TokenVerifier.verify_for_headers(request.headers)
    if not user_profile_token:
        return Response(status=404)

    user_profile = repositories.user_profile_repository.insert(
        transform_to_user_profile(request.json)
    )
    return jsonify(transform_to_json(user_profile))


@USER_ROUTES.route("/api/user/profile", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_user_profile() -> Any:
    user_profile_token = TokenVerifier.verify_for_headers(request.headers)
    if not user_profile_token:
        return Response(status=404)

    result = repositories.user_profile_repository.fetch_user_by_email(
        user_profile_token.email
    )
    if not result:
        return Response(status=401)
    return jsonify(transform_to_json(result))


def transform_to_json(user_profile: UserProfile) -> dict:
    return {
        "email": user_profile.email,
        "avatarUrl": user_profile.avatar_url,
        "familyName": user_profile.family_name,
        "givenName": user_profile.given_name,
    }


def transform_to_user_profile(body: dict) -> UserProfile:
    return UserProfile(
        email=body["email"],
        given_name=body["givenName"],
        family_name=body["familyName"],
        avatar_url=body["avatarUrl"],
    )


@VENUE_API_ROUTES.route("/api/venues", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_venues() -> Any:
    venues = repositories.venue_repository.fetch_all()
    return jsonify({"venues": [_transform(venue) for venue in venues]})


def _transform(venue: Venue) -> Dict:
    return {
        "venue_id": venue.venue_id,
        "city": venue.city,
        "country": venue.country,
        "email": venue.email,
        "name": venue.name,
        "phone": venue.phone,
        "source_url": venue.source_url,
        "lastFetchedDate": venue.convert_utc_to_venue_timezone(
            venue.last_fetched_date
        ).isoformat(),
        "url": venue.url,
    }


@RSS_ROUTES.route("/events.xml")
def fetch_rss() -> Any:
    def generate() -> Generator:
        rss_channel = RSSChannel()
        pre_amble = rss_channel.generate_pre_amble()
        yield pre_amble.replace("</rss>", "").replace("</channel>", "")
        for event in [
            event_entity_transformer.to_event(event)
            for event in repositories.event_repository.fetch_all_rss_items()
        ]:
            yield Transformer.item_to_rss(event).as_node()
        yield rss_channel.generate_post_amble()

    return Response(generate(), mimetype="text/xml")
