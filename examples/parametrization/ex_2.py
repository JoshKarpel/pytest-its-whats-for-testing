# fixtures can be parametrized

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


def test_database(database):
    print(database)
    assert False
