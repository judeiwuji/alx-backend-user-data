#!/usr/bin/env python3
"""Authentication module"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    salt = gensalt(12)
    return hashpw(password.encode(), salt)
