import unittest

from hamcrest.core import assert_that, equal_to

from app.core.user.user_profile import UserProfile
from app.core.user.user_profile_entity_transformer import UserProfileEntityTransformer


class TestUserProfileEntityTransformer(unittest.TestCase):
    @staticmethod
    def fixture() -> UserProfile:
        return UserProfile(
            email="test@test.com", given_name="unittest", family_name="test", avatar_url="http://gravatar.nl/go.jpg"
        )

    def test_transform_to_entity(self):
        user_profile = self.fixture()
        entity = UserProfileEntityTransformer.as_entity(user_profile)
        assert_that(entity["email"], equal_to("test@test.com"))
        assert_that(entity["given_name"], equal_to("unittest"))
        assert_that(entity["family_name"], equal_to("test"))
        assert_that(entity["avatar_url"], equal_to("http://gravatar.nl/go.jpg"))

    def test_entity_to(self):
        user_profile = self.fixture()
        entity = UserProfileEntityTransformer.as_entity(user_profile)
        up = UserProfileEntityTransformer.from_entity(entity)
        assert_that(up.email, equal_to("test@test.com"))
        assert_that(up.given_name, equal_to("unittest"))
        assert_that(up.family_name, equal_to("test"))
        assert_that(up.avatar_url, equal_to("http://gravatar.nl/go.jpg"))
