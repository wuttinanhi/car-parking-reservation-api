"""
    user blueprint
"""


from auth.decorator import admin_only, login_required
from auth.function import GetUser
from flask import Blueprint, request
from pagination.pagination import create_pagination_options_from_request

from user.service import UserService

blueprint = Blueprint("user", __name__, url_prefix="/user")


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
def user():
    user = GetUser()
    return user.json_full()
