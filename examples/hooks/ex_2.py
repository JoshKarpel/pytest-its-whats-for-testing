# hook functions can be combined to do weird things
# example: parametrize based on command-line arguments


def pytest_generate_tests(metafunc):
    if "db" in metafunc.fixturenames:
        metafunc.parametrize(
            argnames="db",
            argvalues=metafunc.config.getoption("db"),
        )


def test_db_type(db):
    assert db == "sqlite3"
