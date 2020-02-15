from typing import Any

from flask import Blueprint, Response, jsonify, request
from flask_cors import cross_origin

from app.application_data import user_profile_repository
from app.core.app_config import AppConfig
from app.core.authorization.token_verifier import TokenVerifier
from app.core.user.user_profile import UserProfile

USER_ROUTES = Blueprint("user", __name__, template_folder="templates")


@USER_ROUTES.route("/api/user/signup", methods=["POST"])
@cross_origin(**AppConfig.cors())
def login_user() -> Any:

    user_profile_token = TokenVerifier.verify_for_headers(request.headers)
    if not user_profile_token:
        return Response(status=404)

    user_profile_in_request = transform_to_user_profile(request.json)
    user_profile = user_profile_repository.fetch_user_by_email(user_profile_in_request.email)
    if user_profile:
        return jsonify(transform_to_json(user_profile))

    user_profile = user_profile_repository.insert(user_profile_in_request)
    return jsonify(transform_to_json(user_profile)), 201


@USER_ROUTES.route("/api/user/profile", methods=["POST"])
@cross_origin(**AppConfig.cors())
def update_user() -> Any:
    user_profile_token = TokenVerifier.verify_for_headers(request.headers)
    if not user_profile_token:
        return Response(status=404)

    user_profile = user_profile_repository.insert(transform_to_user_profile(request.json))
    return jsonify(transform_to_json(user_profile))


@USER_ROUTES.route("/api/user/profile", methods=["GET"])
@cross_origin(**AppConfig.cors())
def fetch_user_profile() -> Any:
    user_profile_token = TokenVerifier.verify_for_headers(request.headers)
    if not user_profile_token:
        return Response(status=404)

    result = user_profile_repository.fetch_user_by_email(user_profile_token.email)
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
        email=body["email"], given_name=body["givenName"], family_name=body["familyName"], avatar_url=body["avatarUrl"]
    )
