"""
    auth decorator
"""

from functools import wraps

from admin.service import AdminService
from flask import request
from werkzeug.exceptions import Unauthorized

from auth.service import AuthService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header == None:
                raise Unauthorized("Unauthorized!")

            jwt_token = auth_header.split("Bearer ")[1]
            if jwt_token == None:
                raise Unauthorized("Unauthorized!")

            user = AuthService.get_user_from_jwt_token(jwt_token)
            request.user = user

            return f(*args, **kwargs)
        except Exception as e:
            raise Unauthorized("Unauthorized!")

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
