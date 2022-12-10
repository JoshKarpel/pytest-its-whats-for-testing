def pytest_addoption(parser):
    parser.addoption(
        "--db",
        action="store",
        nargs="+",
        help="which databases to test against",
        default=["sqlite3"],
        required=False,
    )
