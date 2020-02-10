# pytest can "unwind" the call stack and tell you how a value came to exist


def foo():
    return 5


def test_foo():
    assert foo() == 4
