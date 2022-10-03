"""
    auth blueprint
"""


import os

from flask import Blueprint, request
from jwt_wrapper.service import JwtService
from marshmallow import Schema, fields, validate
from user.service import UserService
from util.validate_request import ValidateRequest

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


class LoginDto(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=5, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=50))


class RegisterDto(LoginDto):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    firstname = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    lastname = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone_number = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    citizen_id = fields.Str(required=True, validate=validate.Length(min=13, max=13))


@blueprint.route("/login", methods=["POST"])
def login():
    data = ValidateRequest(LoginDto, request)
    check = UserService.login(data.email, data.password)

    if check:
        user = UserService.find_by_email(data.email)
        jwt = {"user_id": user.id}
        token: str
        if os.getenv("ENV") != "production":
            token = JwtService.encode(jwt, 86400 * 5)  # 5 days
        else:
            token = JwtService.encode(jwt, 60 * 5)  # 5 minutes
        return {"token": token}, 200
    return {"error": "Invalid login!"}, 401


@blueprint.route("/register", methods=["POST"])
def register():
    data = ValidateRequest(RegisterDto, request)
    UserService.register(
        data.email,
        data.password,
        data.username,
        data.firstname,
        data.lastname,
        data.phone_number,
        data.citizen_id,
    )
    return {"message": "Successfully registered"}, 201
