#!/usr/bin/env python3
"""basic auth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user email and password from decoded Base64 value """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that overloads Auth and retrieves the User instance for a
            request
        """
        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        b64_auth_header = self.extract_base64_authorization_header(auth_header)

        if b64_auth_header is None:
            return None

        decoded_b64_auth_header = self.decode_base64_authorization_header(
            b64_auth_header)

        if decoded_b64_auth_header is None:
            return None

        u_email, u_pwd = self.extract_user_credentials(decoded_b64_auth_header)

        if u_email is None or u_pwd is None:
            return None

        user = self.user_object_from_credentials(u_email, u_pwd)

        return user
