"""
    auth service
"""
from flask import request
from jwt_wrapper.service import JwtService
from user.service import UserService
from werkzeug.exceptions import Unauthorized


class AuthService:
    @staticmethod
    def get_user_from_jwt_token(jwt_token: str):
        check = JwtService.validate(jwt_token)
        if check:
            decoded = JwtService.decode(jwt_token)
            user = UserService.find_by_id(decoded["user_id"])
            request.user = user
            return user
        raise Unauthorized("Unauthorized!")
