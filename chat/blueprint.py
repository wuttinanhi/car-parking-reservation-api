"""
    auth blueprint
"""


from auth.decorator import login_required
from auth.function import get_user
from flask import Blueprint, request
from pagination.pagination import create_pagination_options_from_request
from user.service import UserService

from chat.service import ChatService

blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@blueprint.route("/list", methods=["GET"])
@login_required
def list_chat():
    response = []
    user = get_user()
    pagination_options = create_pagination_options_from_request(request)
    result = ChatService.list_chat_head(user, pagination_options)

    for chat_head in result:
        new_json = chat_head.json_populated()
        from_user = UserService.find_by_id(chat_head.user_id)
        to_user = UserService.find_by_id(chat_head.target_user_id)
        last_chat = ChatService.get_last_chat_message(from_user, to_user)
        new_json["last_chat"] = last_chat.json()
        response.append(new_json)

    return response
