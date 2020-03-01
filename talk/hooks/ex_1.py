# pytest exposes hook functions for a lot of its internal behavior
# example: parametrization is just hooking into pytest_generate_tests

import pytest
import os


def pytest_generate_tests(metafunc):
    if "foo" in metafunc.fixturenames:
        metafunc.parametrize("foo", ['foobar', 'wizbang'])


def test_it(foo):
    assert foo == 'foobar'
