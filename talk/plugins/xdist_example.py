import pytest

import time


@pytest.mark.parametrize("x", range(100))
def test_foo(x):
    time.sleep(0.1)
    assert True
