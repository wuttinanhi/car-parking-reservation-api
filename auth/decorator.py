"""
    auth decorator
"""

from functools import wraps

from admin.service import AdminService
from flask import request
from jwt_wrapper.service import JwtService
from user.service import UserService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header == None:
            return {"error": "Unauthorized!"}, 401

        jwt_token = auth_header.split("Bearer ")[1]
        check = JwtService.validate(jwt_token)

        if check:
            decoded = JwtService.decode(jwt_token)
            user = UserService.find_by_id(decoded["user_id"])
            request.user = user
            return f(*args, **kwargs)
        return {"error": "Unauthorized!"}, 401

    return decorated_function


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("X-API-KEY")
        if auth_header == None:
            return {"error": "Unauthorized!"}, 401

        admin_key = auth_header
        check = AdminService.is_valid_admin_key(admin_key)

        if check:
            return f(*args, **kwargs)

        return {"error": "Unauthorized!"}, 401

    return decorated_function
