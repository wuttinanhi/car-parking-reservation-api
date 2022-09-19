"""
    auth function wrapper
"""

from flask import request
from user.model import User


def GetUser() -> User:
    return request.user
