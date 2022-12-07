# fixtures are nonlocal (this should scare you)


def test_fixture_from_elsewhere(where_am_i_from):
    assert where_am_i_from == "?"
