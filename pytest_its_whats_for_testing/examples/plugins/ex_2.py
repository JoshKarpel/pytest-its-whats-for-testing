# pytest-timeout helps you do test-level timeouts

import time

import pytest


@pytest.mark.timeout(1)
def test_sleep():
    time.sleep(2)
    assert True
