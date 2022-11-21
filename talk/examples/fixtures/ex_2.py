# fixtures can hold a context
# the cleanup happens even if the test fails!

import pytest


@pytest.fixture
def file():
    print(f"before with block")
    with open(__file__, mode="r") as file:
        print(f"start with block")
        yield file
        print(f"back in the with block")
    print("after with block")


def test_the_file(file):
    print("in the test")
    assert False
