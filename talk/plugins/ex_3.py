# hypothesis is lets you do property-based testing

import pytest

import hypothesis
from hypothesis import strategies


def truncate(string, length):
    if 'x' in string:
        return string
    return string[:length]


@pytest.mark.parametrize(
    'string, length',
    [
        ('foobar', 3),
        ('wizbang', 4),
        ('short', 10),
    ]
)
def test_truncate(string, length):
    result = truncate(string, length)
    assert len(result) <= length


# @hypothesis.given(
#     string = strategies.text(),
#     length = strategies.integers(),
# )
# def test_truncate_with_hypothesis(string, length):
#     result = truncate(string, length)
#     assert len(result) <= length
