from dataclasses import dataclass
from typing import Optional, Dict

from google.cloud import datastore
from google.cloud.client import Client


@dataclass
class UserProfile:
    given_name: str
    family_name: str
    email: str
    avatar_url: str

    def __str__(self) -> str:
        return f"UserProfile email={self.email}"


class UserProfileRepository:
    def __init__(self, client: Client):
        self.client = client

    def fetch_user_by_email(self, email: str) -> Optional[UserProfile]:
        query = self.client.query(kind="User")
        query.add_filter("email", "=", email)
        result = list(query.fetch())
        if not result:
            return None
        return UserProfileEntityTransformer.from_entity(result[0])

    def insert(self, user_profile: UserProfile) -> UserProfile:
        entity = datastore.Entity(self.client.key("User", user_profile.email))
        entity.update(UserProfileEntityTransformer.as_entity(user_profile))
        self.client.put(entity)
        return UserProfileEntityTransformer.from_entity(entity)


class UserProfileEntityTransformer:
    @staticmethod
    def as_entity(user_profile: UserProfile) -> Dict:
        return {
            "email": user_profile.email,
            "given_name": user_profile.given_name,
            "family_name": user_profile.family_name,
            "avatar_url": user_profile.avatar_url,
        }

    @staticmethod
    def from_entity(entity: Dict) -> UserProfile:
        return UserProfile(
            email=entity["email"],
            given_name=entity["given_name"],
            family_name=entity["family_name"],
            avatar_url=entity["avatar_url"],
        )
