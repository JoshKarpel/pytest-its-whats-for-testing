import pytest
import time

@pytest.mark.parametrize('x', range(100))
def test_foo(x):
    time.sleep(.1)
    assert True
