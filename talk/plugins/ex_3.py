# pytest-mock wraps the stdlib unittest.mock module, plus some extras

from pathlib import Path

import pytest


def test_mock(mocker):
    assert Path("this-file-does-not-exist").exists()


class Multiplier:
    def double(self, x):
        return 2 * x

    def quadruple(self, x):
        return self.double(self.double(x))


def test_spy(mocker):
    mult = Multiplier()

    result = mult.quadruple(2)

    assert result == 8
