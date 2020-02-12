# fixtures are "shared setup functions"

import pytest


class User:
    def __init__(self, email, is_admin):
        self.email = email
        self.is_admin = is_admin


def test_user_is_josh():
    assert user.email == "josh@example.com"


def test_josh_is_admin():
    assert user.is_admin
