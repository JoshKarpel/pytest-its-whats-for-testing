# parametrization is combinatoric

import pytest


@pytest.fixture(
    params=[
        "sqlite",
        "postgres",
        "mongo",
    ]
)
def database(request):
    return request.param


@pytest.fixture(
    params=[
        "josh",
        "ed",
    ]
)
def username():
    return "josh"


def test_something(database, username):
    pass
