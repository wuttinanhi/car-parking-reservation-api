"""
    auth function wrapper
"""

from flask import request
from user.model import User


def get_user() -> User:
    return request.user
