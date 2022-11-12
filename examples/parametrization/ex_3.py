# parametrization is combinatoric

import pytest


@pytest.fixture(params=["sqlite", "postgres", "mongo"])
def database(request):
    return request.param


@pytest.fixture()
def username():
    return "josh"


def test_database_and_username(database, username):
    pass
