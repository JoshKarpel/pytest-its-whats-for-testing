# fixtures have scope
# we can see the scoping by running
#  $ pytest --setup-show/plan

import pytest


@pytest.fixture(scope="session")
def session():
    pass


@pytest.fixture(scope="module")
def module(session):
    pass


@pytest.fixture(scope="function")
def function(session, module):
    pass


def test_a(session, module, function):
    pass


def test_b(session, module, function):
    pass
