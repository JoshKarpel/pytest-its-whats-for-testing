# pytest comes with lots of fixtures out of the box

import pytest


def test_dir(tmp_path):
    assert (tmp_path / 'nope').exists()
