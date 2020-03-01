def pytest_addoption(parser):
    parser.addoption(
        "--db_types",
        action = 'store',
        nargs = '+',
        help = "which databases to test against",
        default = ['sqlite3'],
        required = False,
    )


def pytest_generate_tests(metafunc):
    if 'db_type' in metafunc.fixturenames:
        metafunc.parametrize(
            "db_type",
            metafunc.config.getoption("db_types"),
        )
