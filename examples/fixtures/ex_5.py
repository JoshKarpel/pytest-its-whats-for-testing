# fixtures have scope
# we can see the scoping by running pytest --setup-show/plan

import pytest


@pytest.fixture(scope="module")
def module_fixture():
    pass


@pytest.fixture(scope="function")
def function_fixture():
    pass


def test_a(module_fixture, function_fixture):
    pass


def test_b(module_fixture, function_fixture):
    pass
