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
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if path.endswith('/'):
            path = path[0: -1]
        if path in excluded_paths or path + '/' in excluded_paths\
                or self.wild_path_match(path, excluded_paths):
            return False
        return True

    def wild_path_match(self, path: str, excluded_paths: List[str]) -> bool:
        """match wild character"""
        for d in excluded_paths:
            if d.endswith("*"):
                if path[:len(d) - 1] + '*' == d:
                    return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns
         - authorization token
        """
        if request is None:
            return None
        return request.headers.get("authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns
         - current logged in user
        """
        return None
