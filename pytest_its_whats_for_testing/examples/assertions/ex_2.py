# pytests "peek" inside containers to provide diffs


def test_list_equality():
    assert [1, 2, 3] == [1, 2, 3, 4]


def test_dict_equality():
    assert {"a": 1, "b": 1} == {"a": 1}
