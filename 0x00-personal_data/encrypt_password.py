#!/usr/bin/env python3
"""Module: Encrypt password"""
from typing import ByteString
from bcrypt import gensalt, hashpw


def hash_password(password: str) -> ByteString:
    """hash a given password"""
    salt = gensalt(12)
    return hashpw(password.encode("utf-8"), salt)
