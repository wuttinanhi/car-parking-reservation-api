'''
    auth blueprint
'''


import os
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR

from flask import Blueprint, request
from jwt_wrapper.service import JwtService
from marshmallow import Schema, ValidationError, fields, validate
from user.service import UserService
from util.validate_request import ValidateRequest
from werkzeug.exceptions import HTTPException

from auth.decorator import login_required
from auth.function import GetUser

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


class LoginDto(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=50)
    )


class RegisterDto(LoginDto):
    pass


@blueprint.route('/login', methods=['POST'])
def login():
    data = ValidateRequest(LoginDto, request)
    check = UserService.login(data.email, data.password)

    if check:
        user = UserService.find_by_email(data.email)
        jwt = {"user_id": user.id}
        token: str
        if os.getenv("ENV") != "production":
            token = JwtService.encode(jwt, 86400*5)  # 5 days
        else:
            token = JwtService.encode(jwt, 60*5)  # 5 minutes
        return {'token': token}, 200
    return {"message": "Invalid login!"}, 401


@blueprint.route('/register', methods=['POST'])
def register():
    data = ValidateRequest(LoginDto, request)
    UserService.register(data.email, data.password)
    return {'message': "Successfully registered"}, 201


@blueprint.route('/user', methods=['GET'])
@login_required
def user():
    user = GetUser()
    return user.email


@blueprint.errorhandler(Exception)
def error_handle(err: Exception):
    if issubclass(type(err), ValidationError):
        return str(err), BAD_REQUEST
    if issubclass(type(err), HTTPException):
        return {'error': err.description}, err.code
    return {'message': "Internal server exception!"}, INTERNAL_SERVER_ERROR
