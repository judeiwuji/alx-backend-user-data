#!/usr/bin/env python3
"""Module: Encrypt password"""
from typing import ByteString
from bcrypt import gensalt, hashpw, checkpw


def hash_password(password: str) -> ByteString:
    """hash a given password"""
    salt = gensalt(12)
    return hashpw(password.encode("utf-8"), salt)


def is_valid(hashed_password: ByteString, password: str) -> bool:
    """validate that the provided password matches\
    the hashed password."""
    return checkpw(password.encode("utf-8"), hashed_password)
