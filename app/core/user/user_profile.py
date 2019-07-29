from dataclasses import dataclass


@dataclass
class UserProfile:
    given_name: str
    family_name: str
    email: str
    avatar_url: str

    def __str__(self):
        return f'UserProfile email={self.email}'
