"""
    auth decorator
"""

from functools import wraps

from flask import request
from jwt_wrapper.service import JwtService
from user.service import UserService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header == None:
            return {"message": "Unauthorized!"}, 401

        jwt_token = auth_header.split("Bearer ")[1]
        check = JwtService.validate(jwt_token)

        if check:
            decoded = JwtService.decode(jwt_token)
            user = UserService.find_by_id(decoded["user_id"])
            request.user = user
            return f(*args, **kwargs)
        return {"message": "Unauthorized!"}, 401

    return decorated_function
