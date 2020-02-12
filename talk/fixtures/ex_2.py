# fixtures can hold a context
# the cleanup happens even if the test fails!

import pytest


@pytest.fixture
def transaction():
    txn = object()
    print(f"fixture created {txn}")

    yield txn

    print(f"back in the fixture with {txn}")


def test_the_database(transaction):
    assert transaction
