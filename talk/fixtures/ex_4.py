# fixtures can depend on other fixtures

import pytest


@pytest.fixture
def parent():
    pass


@pytest.fixture
def child(parent):
    pass


def test_foo(child):
    pass
