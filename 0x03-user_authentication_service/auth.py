#!/usr/bin/env python3
"""auth module"""
from bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_passwword(password: str) -> bytes:
    """return the hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """a method to registr a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_passwword(password))
        else:
            raise ValueError(f"User {email} already exists")
