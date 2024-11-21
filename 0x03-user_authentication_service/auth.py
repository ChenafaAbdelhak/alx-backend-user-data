#!/usr/bin/env python3
"""auth module"""
from bcrypt


def _hash_passwword(password: str) -> bytes:
    """return the hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
