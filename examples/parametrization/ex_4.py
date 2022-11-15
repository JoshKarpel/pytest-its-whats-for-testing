# customized combinatorics via itertools

from itertools import combinations_with_replacement

import pytest

TYPES = combinations_with_replacement(
    [
        "radial",
        "grad",
        "cross",
    ],
    r=2,
)
LM = [(l, m) for l in range(3) for m in range(-l, l + 1)]


@pytest.mark.parametrize("type_a, type_b", TYPES)
@pytest.mark.parametrize("l_a, m_a", LM)
@pytest.mark.parametrize("l_b, m_b", LM)
def test_integral_orthonormalization(
    type_a,
    type_b,
    l_a,
    m_a,
    l_b,
    m_b,
):
    pass
