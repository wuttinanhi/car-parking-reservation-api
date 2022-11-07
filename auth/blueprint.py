"""
    auth blueprint
"""


import os

from flask import Blueprint, request
from jwt_wrapper.service import JwtService
from marshmallow import Schema, fields, validate
from user.service import UserService
from util.validate_request import validate_request
from werkzeug.exceptions import Unauthorized

from auth.decorator import admin_only, login_required
from auth.function import get_user

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


class ChangePasswordDto(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=8, max=50))
    new_password = fields.Str(required=True, validate=validate.Length(min=8, max=50))


class AdminChangePasswordDto(ChangePasswordDto):
    user_id = fields.Int(required=True)


@blueprint.route("/login", methods=["POST"])
def login():
    data = validate_request(LoginDto, request)
    check = UserService.login(data.email, data.password)

    if check:
        user = UserService.find_by_email(data.email)
        jwt = {"user_id": user.id}
        token: str
        if os.getenv("ENV") != "production":
            token = JwtService.encode(jwt, 86400 * 5)  # 5 days
        else:
            token = JwtService.encode(jwt, 86400)  # TEMP INCREASE TO 1 DAY
        return {"token": token}, 200
    return {"error": "Invalid login!"}, 401


@blueprint.route("/register", methods=["POST"])
def register():
    data = validate_request(RegisterDto, request)
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


@blueprint.route("/changepassword", methods=["PATCH"])
@login_required
def change_password():
    user = get_user()
    data = validate_request(ChangePasswordDto, request)

    check_password = UserService.compare_password(user, data.password)
    if check_password is False:
        raise Unauthorized("Invalid password!")

    UserService.change_password(user, data.new_password)

    return {"message": "Successfully change password."}, 200


@blueprint.route("/admin/changepassword", methods=["PATCH"])
@admin_only
def admin_change_password():
    data = validate_request(AdminChangePasswordDto, request)
    user = UserService.find_by_id(data.user_id)
    UserService.change_password(user, data.new_password)
    return {"message": "Successfully change password."}, 200
