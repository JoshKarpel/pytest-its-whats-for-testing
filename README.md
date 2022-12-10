# pytest-its-whats-for-testing

The repository contains a [Spiel](https://github.com/JoshKarpel/spiel) presentation
that I gave at [MadPy](https://madpy.com/meetups/2022/12/8/20221208-pytest-its-whats-for-testing/) in December 2022
about [pytest](https://docs.pytest.org/).

You can run the slides yourself using Docker (or equivalent):

```console
$ docker run -it --rm ghcr.io/joshkarpel/pytest-its-whats-for-testing:2022-12-08-madpy
```

or by installing this repository using `pip` and running the `slides` submodule:
```console
$ pip install git+https://github.com/JoshKarpel/pytest-its-whats-for-testing
$ python -m pytest_its_whats_for_testing.slides
```

(You may need to [install some extra system packages](https://simpleaudio.readthedocs.io/en/latest/installation.html#linux-dependencies) if you're on Linux.)
