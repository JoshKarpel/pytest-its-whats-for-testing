# example: parametrization is hooking into pytest_generate_tests


def pytest_generate_tests(metafunc):
    if "foo" in metafunc.fixturenames:
        metafunc.parametrize(
            argnames="foo",
            argvalues=["foobar", "wizbang"],
        )


def test_it(foo):
    assert foo == "foobar"
