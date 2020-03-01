# combine multiple hook functions to get information where it needs to go
# example: parametrize based on command-line arguments

import pytest
import os


@pytest.fixture
def db(db_type):
    if db_type == 'postgresql':
        return object()
    elif db_type == 'sqlite3':
        return object()
    # ...


def test_foo(db):
    assert db
