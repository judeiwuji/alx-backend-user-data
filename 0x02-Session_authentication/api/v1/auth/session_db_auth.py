#!/usr/bin/env python3
"""
Session DB Authentication module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import timedelta, datetime


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication class"""

    def create_session(self, user_id=None):
        """creates a Session ID for a user_id"""
        from models.user_session import UserSession
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns
         - User ID based on a Session ID
        """
        if session_id is None:
            return None

        from models.user_session import UserSession
        session = None
        try:
            sessions = UserSession.search({'session_id': session_id})
            if len(sessions) > 0:
                session = sessions[0]
        except Exception:
            return None
        from sys import stdout
        if session is None:
            return None

        if self.session_duration <= 0:
            return session.user_id

        if session.created_at is None:
            return None
        duration = session.created_at + \
            timedelta(seconds=self.session_duration)

        if duration < datetime.utcnow():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """
        deletes the user session / logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        from models.user_session import UserSession
        sessions = UserSession.search({'session_id': session_id})
        if len(sessions) == 0:
            return False
        sessions[0].remove()
        return True
