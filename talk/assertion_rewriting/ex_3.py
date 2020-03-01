# pytest can "unwind" the call stack and tell you how a value came to exist


def test_foo():
    with open('file.txt', mode = 'w') as f:
        assert f.write('foo') > 0
