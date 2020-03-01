# fixtures can hold a context
# the cleanup happens even if the test fails!

import pytest


@pytest.fixture
def file():
    with open('foo/file.txt', mode = 'w') as file:
        print(f"fixture created {file}")
        yield file
        print(f"back in the fixture with {file}")
    print('after with block')


def test_the_file(file):
    assert file.write('hello') > 0
