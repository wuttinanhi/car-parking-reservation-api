"""
    auth decorator
"""

from functools import wraps

from flask import request
from services.jwt_wrapper.jwt_wrapper import JwtWrapper
from services.user.user import UserService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt_token = request.headers.get("Authorization").split("Bearer ")[1]
        check = JwtWrapper.validate(jwt_token)

        if check:
            decoded = JwtWrapper.decode(jwt_token)
            user = UserService.find_by_id(decoded["user_id"])
            request.user = user
            return f(*args, **kwargs)
        return {"message": "Unauthorized!"}, 401

    return decorated_function
