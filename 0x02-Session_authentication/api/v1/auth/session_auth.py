#!/usr/bin/env python3
"""module for session authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        session_cookie = self.session_cookie(request)

        if session_cookie is None:
            return None
        user_id = self.user_id_for_session_id(session_cookie)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy a session"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)

        if not session_cookie:
            return False
        
        if not self.user_id_for_session_id(session_cookie):
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
