import pytest

from pathlib import Path


@pytest.fixture
def where_am_i_from():
    return Path(__file__).name
