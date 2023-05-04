#!/usr/bin/env python3
"""
Session Expire Authentication module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Session Expire Authentication class
    """

    def __init__(self):
        """create session expire instance"""
        super()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns
         - User ID based on a Session ID
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        user_id = session_dictionary.get('user_id')
        if self.session_duration <= 0:
            return user_id

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        duration = created_at + timedelta(seconds=self.session_duration)
        if duration < datetime.now():
            return None
        return user_id
