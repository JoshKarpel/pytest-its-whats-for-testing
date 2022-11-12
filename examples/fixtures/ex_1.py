# fixtures are "shared setup functions"
# use them to reduce duplication and clarify intent


from dataclasses import dataclass

import pytest


@dataclass
class User:
    email: str
    is_admin: bool


@pytest.fixture
def user():
    return User(email="josh@example.com", is_admin=True)


def test_user_is_josh(user):
    assert user.email == "gosh@example.com"


def test_josh_is_admin(user):
    assert user.is_admin
