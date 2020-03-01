# parametrization reduces duplication

import pytest


def is_valid_email(email):
    return all(("@" in email, email.endswith(".com") or email.endswith(".edu")))


def test_validate_email_1():
    email = "josh@example.com"
    assert is_valid_email(email)


def test_validate_email_2():
    email = "josh@example.edu"
    assert is_valid_email(email)


def test_validate_email_3():
    email = "josh@example.net"
    assert not is_valid_email(email)


def test_validate_email_4():
    email = "josh.example.net"
    assert not is_valid_email(email)
