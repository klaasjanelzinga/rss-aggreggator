import asyncio
import logging
from typing import Dict, Optional

import aiohttp
from google.auth import jwt
from werkzeug.datastructures import EnvironHeaders

from app.core.user.user_profile import UserProfile


class TokenVerificationException(Exception):
    pass


class TokenVerifier:

    @staticmethod
    async def _fetch_certs() -> Dict:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as task_session:
            async with task_session.get('https://www.googleapis.com/oauth2/v1/certs') as response:
                return await response.json()

    @staticmethod
    async def _verify(headers: Dict) -> Optional[UserProfile]:
        token_certs_task = asyncio.create_task(TokenVerifier._fetch_certs())
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
                                certs=await token_certs_task,
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
        finally:
            if not token_certs_task.done():
                token_certs_task.cancel()
        return None

    @staticmethod
    def verify_for_headers(headers: EnvironHeaders) -> Optional[UserProfile]:
        result = asyncio.run(TokenVerifier._verify(dict(headers)))
        return result
