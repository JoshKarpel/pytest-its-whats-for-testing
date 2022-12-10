# parametrization reduces duplication

import pytest


def is_valid_email(email):
    return all(
        (
            "@" in email,
            email.endswith(".com") or email.endswith(".edu"),
        )
    )


@pytest.mark.parametrize(
    "email, result",
    [
        ("josh@example.com", True),
        ("josh@example.edu", True),
        ("josh@example.net", False),
        ("josh.example.com", False),
    ],
)
def test_is_valid_email(email, result):
    assert is_valid_email(email) is result
