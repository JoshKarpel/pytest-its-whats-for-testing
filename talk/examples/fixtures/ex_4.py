# fixtures can depend on other fixtures

import pytest


@pytest.fixture
def parent():
    return 1


@pytest.fixture
def child(parent):
    return parent + 2


def test_foo(child):
    assert child == 3
