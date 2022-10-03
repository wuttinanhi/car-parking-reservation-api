"""
    auth blueprint
"""


from auth.decorator import login_required
from auth.function import GetUser
from flask import Blueprint, request
from pagination.pagination import create_pagination_options_from_request

from chat.service import ChatService

blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@blueprint.route("/list", methods=["GET"])
@login_required
def list_chat():
    response = []
    user = GetUser()
    pagination_options = create_pagination_options_from_request(request)
    result = ChatService.list_chat_head(user, pagination_options)
    for chat_head in result:
        response.append(chat_head.json_populated())
    return response
