#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Ensures that a route user is authenticated
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns
         - authorization token
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns
         - current logged in user
        """
        return None
