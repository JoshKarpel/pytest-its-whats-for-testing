# this works for dataclasses too!


from dataclasses import dataclass


@dataclass
class Foo:
    s: str
    i: int


def test_foo():
    assert Foo(s="a", i=1) == Foo(s="b", i=1)
