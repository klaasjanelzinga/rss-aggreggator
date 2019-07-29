import logging
from typing import Dict, Optional

import requests
from google.auth import jwt

from app.core.user.user_profile import UserProfile


class TokenVerificationException(Exception):
    pass


class TokenVerifier:

    @staticmethod
    def fetch_certs() -> Dict:
        return requests.get('https://www.googleapis.com/oauth2/v1/certs').json()

    @staticmethod
    def verify(headers: Dict) -> Optional[UserProfile]:
        try:
            if 'Authorization' not in headers:
                raise TokenVerificationException('Authorization header is not set')
            bearer_token: str = headers['Authorization']
            if len(bearer_token) < 15:
                raise TokenVerificationException('Unlikely content of authorization header')
            if not bearer_token.startswith('Bearer'):
                raise TokenVerificationException('Unlikely content of authorization header')
            token = bearer_token[7:]
            result = jwt.decode(token=token,
                                certs=TokenVerifier.fetch_certs(),
                                audience='274288767473-3csldch2v5qm7v15b35f25325cqtbp7f.apps.googleusercontent.com')
            return UserProfile(
                given_name=result['given_name'],
                family_name=result['family_name'],
                email=result['email'],
                avatar_url=result['picture']
            )
        except ValueError as error:
            logging.info('JWT validation failed %s', error.__str__())
        except TokenVerificationException as error:
            logging.info('JWT validation failed %s', error.__str__())
        return None
