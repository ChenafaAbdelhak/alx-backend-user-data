#!/usr/bin/env python3
"""module for session authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """a class to implement the session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a sesion id for a user"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id
