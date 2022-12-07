# hypothesis lets you write property tests
# (think parametrization, but guided by the computer)

from hypothesis import given
from hypothesis import strategies as st


@given(st.floats(), st.floats())
def test_float_add_is_commutative(x, y):
    assert x + y == y + x
