from typing import Optional

from google.cloud import datastore
from google.cloud.client import Client

from app.core.user.user_profile import UserProfile
from app.core.user.user_profile_entity_transformer import UserProfileEntityTransformer


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
