#!/usr/bin/env python3
"""Auth module"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required. """
        if path is None:
            return True

        if not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> None:
        """ Returns the value of the Authorization header. """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> None:
        """ Returns the current user (to be implemented later). """
        return None
