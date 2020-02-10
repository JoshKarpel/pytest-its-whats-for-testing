def test():
    assert 1 == 1


###


@pytest.fixture
def db():
    db = Database()
    yield db
    db.rollback()


def test(db):
    db.insert()


###


@pytest.mark.parametrize("input, output", [(1, 2), (2, 4)])
def test(input, output):
    assert input * 2 == output


###


def pytest_generate_tests(metafunc):
    if "range" in metafunc.fixturenames:
        metafunc.parametrize("range", [list(range(n)) for n in range(5)])


def test(range):
    assert sum(range) == range[-1] * (range[-1] + 1) / 2
