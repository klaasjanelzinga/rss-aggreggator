from hamcrest.core import assert_that, equal_to

from core_lib.core.user.user_profile import UserProfile
from core_lib.core.user.user_profile_entity_transformer import UserProfileEntityTransformer


def test_transform_to_entity(valid_user_profile: UserProfile):
    entity = UserProfileEntityTransformer.as_entity(valid_user_profile)
    assert_that(entity["email"], equal_to(valid_user_profile.email))
    assert_that(entity["given_name"], equal_to(valid_user_profile.given_name))
    assert_that(entity["family_name"], equal_to(valid_user_profile.family_name))
    assert_that(entity["avatar_url"], equal_to(valid_user_profile.avatar_url))


def test_entity_to(valid_user_profile):
    entity = UserProfileEntityTransformer.as_entity(valid_user_profile)
    up = UserProfileEntityTransformer.from_entity(entity)
    assert_that(up.email, equal_to(valid_user_profile.email))
    assert_that(up.given_name, equal_to(valid_user_profile.given_name))
    assert_that(up.family_name, equal_to(valid_user_profile.family_name))
    assert_that(up.avatar_url, equal_to(valid_user_profile.avatar_url))
