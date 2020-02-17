# pytest-timeout helps you do test-level timeouts

import pytest

import time


@pytest.mark.timeout(5)
def test_sleep():
    time.sleep(6)
    assert True
