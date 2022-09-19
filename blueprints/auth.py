'''
    auth blueprint
'''


from flask import Blueprint, request
from marshmallow import Schema, ValidationError, fields, validate
from services.auth.decorator import login_required
from services.jwt_wrapper.jwt_wrapper import JwtWrapper
from services.user.user import UserService
from util.validate_request import ValidateRequest

bp = Blueprint("auth", __name__, url_prefix="/auth")


class LoginDto(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=50)
    )


class RegisterDto(LoginDto):
    pass


@bp.route('/login', methods=['POST'])
def login():
    data = ValidateRequest(LoginDto, request)
    check = UserService.login(data.email, data.password)

    if check:
        user = UserService.find_by_email(data.email)
        jwt = {"user_id": user.id}
        token = JwtWrapper.encode(jwt, 60*5)
        return {'token': token}, 200
    return {"message": "Invalid login!"}, 401


@bp.route('/register', methods=['POST'])
def register():
    data = ValidateRequest(LoginDto, request)
    UserService.register(data.email, data.password)
    return {'message': "Successfully registered"}, 201


@bp.route('/user', methods=['GET'])
@login_required
def user():
    # jwt_token = request.headers.get("Authorization").split("Bearer ")[1]
    # check = JwtWrapper.validate(jwt_token)

    # if check:
    #     decoded = JwtWrapper.decode(jwt_token)
    #     user = UserService.find_by_id(decoded["user_id"])
    #     return {"id": user.id, "email": user.email}, 200
    # return {"message": "Unauthorized!"}, 401
    user = request.user
    return user.email


@bp.errorhandler(Exception)
def error_handle(err: Exception):
    if err.__class__ is ValidationError:
        return str(err), 400
    return {'message': "Internal server exception!", "error": str(err)}, 500
