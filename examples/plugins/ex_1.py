# pytest-xdist parallelizes your tests

import time

import pytest


@pytest.mark.parametrize("x", range(100))
def test_foo(x):
    time.sleep(0.1)
    assert True
