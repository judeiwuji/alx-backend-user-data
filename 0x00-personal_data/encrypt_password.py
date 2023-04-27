#!/usr/bin/env python3
"""Module: Encrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash a given password"""
    salt = bcrypt.gensalt(12)
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches
    the hashed password."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
