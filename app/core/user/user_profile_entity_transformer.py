from typing import Dict

from app.core.user.user_profile import UserProfile


class UserProfileEntityTransformer:

    @staticmethod
    def as_entity(user_profile: UserProfile) -> Dict:
        return {
            'email': user_profile.email,
            'given_name': user_profile.given_name,
            'family_name': user_profile.family_name,
            'avatar_url': user_profile.avatar_url
        }

    @staticmethod
    def from_entity(entity: Dict) -> UserProfile:
        return UserProfile(email=entity['email'],
                           given_name=entity['given_name'],
                           family_name=entity['family_name'],
                           avatar_url=entity['avatar_url'])
