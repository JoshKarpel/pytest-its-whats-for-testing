# dark magic: parametrize a fixture from a test

import pytest


@pytest.fixture
def fix(b):
    return b.upper()


@pytest.mark.parametrize(
    "a, b, result",
    [
        ("foo", "bar", "fooBAR"),
        ("foo", "biz", "fooBIZ"),
    ],
)
def test_combining(a, fix, result) -> None:
    assert f"{a}{fix}" == result
