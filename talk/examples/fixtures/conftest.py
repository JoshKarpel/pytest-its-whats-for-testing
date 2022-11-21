from pathlib import Path

import pytest


@pytest.fixture
def where_am_i_from():
    return Path(__file__).name
