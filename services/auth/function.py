"""
    auth function wrapper
"""

from flask import request
from services.user.user import User


def GetUser() -> User:
    return request.user
