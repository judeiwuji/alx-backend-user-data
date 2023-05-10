#!/usr/bin/env python3
"""Authentication module"""
from db import DB
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    salt = gensalt(12)
    return hashpw(password.encode(), salt)


def _generate_uuid() -> str:
    """
    Return
     - a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """"Initialize an Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creates a new session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Returns
         - the corresponding User or None
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id) -> None:
        """Destroys a specific user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """returns a token string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """updates user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_password,
                reset_token=None)
        except NoResultFound:
            raise ValueError
