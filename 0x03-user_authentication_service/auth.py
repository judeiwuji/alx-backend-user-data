#!/usr/bin/env python3
"""Authentication module"""
from db import DB
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    salt = gensalt(12)
    return hashpw(password.encode(), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """"Initialize an Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str):
        """Creates a new user account"""
        email_exists = None
        try:
            email_exists = self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        if email_exists is not None:
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        return self._db.add_user(email, hashed_password)
