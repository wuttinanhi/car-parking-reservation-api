"""
    user blueprint
"""


from auth.decorator import admin_only, login_required
from auth.function import get_user
from flask import Blueprint, request
from marshmallow import Schema, fields, validate
from pagination.pagination import create_pagination_options_from_request
from util.validate_request import validate_request

from user.service import UserService

blueprint = Blueprint("user", __name__, url_prefix="/user")


class UpdateUserDto(Schema):
    firstname = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    lastname = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone_number = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    citizen_id = fields.Str(required=True, validate=validate.Length(min=13, max=13))


class AdminUpdateUserDto(UpdateUserDto):
    user_id = fields.Int(required=True)


@blueprint.route("/admin/search", methods=["GET"])
@admin_only
def admin_user_search():
    response = []
    pagination_options = create_pagination_options_from_request(request)
    result = UserService.paginate_user(pagination_options)
    for user in result:
        response.append(user.json_full())
    return response


@blueprint.route("/me", methods=["GET"])
@login_required
def user_detail():
    user = get_user()
    return user.json_full()


@blueprint.route("/update", methods=["PATCH"])
@login_required
def update_user():
    user = get_user()
    data = validate_request(UpdateUserDto, request)

    user.firstname = data.firstname
    user.lastname = data.lastname
    user.phone_number = data.phone_number
    user.citizen_id = data.citizen_id

    UserService.update(user)
    return {"message": "Successfully updated user."}, 200


@blueprint.route("/admin/update", methods=["PATCH"])
@admin_only
def admin_update_user():
    data = validate_request(AdminUpdateUserDto, request)
    user = UserService.find_by_id(data.user_id)

    user.firstname = data.firstname
    user.lastname = data.lastname
    user.phone_number = data.phone_number
    user.citizen_id = data.citizen_id

    UserService.update(user)
    return {"message": "Successfully updated user."}, 200
