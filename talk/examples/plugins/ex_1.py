# pytest-mock wraps the stdlib unittest.mock module


class C:
    def m(self):
        return False


def test_mock(mocker):
    c = C()

    assert not c.m()

    mocked_method = mocker.patch.object(
        c,
        "m",
        mocker.Mock(return_value=True),
    )

    assert c.m()

    assert mocked_method.call_count == 1
