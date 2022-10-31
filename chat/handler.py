"""
    chat socket handler
"""

from typing import Any, Dict

from auth.service import AuthService
from flask import request
from flask_socketio import Namespace, emit
from pagination.pagination import int_to_sort
from user.model import User
from user.service import UserService
from util.validate_request import validate_object
from werkzeug.exceptions import NotFound, Unauthorized

from chat.service import ChatHistoryPaginationOptions, ChatService


class ChatMapper(Namespace):
    user_sid_map = {}
    sid_user_map = {}

    @staticmethod
    def register(user: User, sid: str):
        is_exists = ChatMapper.user_sid_map.get(user.id, None)
        if is_exists:
            ChatMapper.remove(user)
        ChatMapper.user_sid_map[user.id] = sid
        ChatMapper.sid_user_map[sid] = user

    @staticmethod
    def remove(user: User):
        sid = ChatMapper.user_sid_map.get(user.id, None)
        if sid:
            del ChatMapper.user_sid_map[user.id]
            del ChatMapper.sid_user_map[sid]

    @staticmethod
    def from_user_to_sid(user: User) -> str:
        sid = ChatMapper.user_sid_map.get(user.id, None)
        if sid is None:
            raise NotFound("user_to_sid")
        return sid

    @staticmethod
    def from_sid_to_user(sid: str) -> User:
        user = ChatMapper.sid_user_map.get(sid, None)
        if user is None:
            raise NotFound("sid_to_user")
        return user

    @staticmethod
    def emit(user: User, event_name: str, data):
        sid = ChatMapper.from_user_to_sid(user)
        emit(event_name, data, to=sid)


class ChatHandler(ChatMapper):
    @staticmethod
    def auth_user(data):
        user: User
        try:
            user = AuthService.get_user_from_jwt_token(data["jwt_token"])
            return user
        except Exception as e:
            raise Unauthorized("Invalid Jwt")

    def on_connect(self):
        print(f"Chat Client connected: {request.sid}")

    def on_disconnect(self):
        sid = request.sid
        user = ChatHandler.from_sid_to_user(sid)
        ChatHandler.remove(user)
        print(f"Chat Client disconnected: {user.id} {user.email} {request.sid}")

    def on_login(self, data):
        user = ChatHandler.auth_user(data)
        sid = request.sid
        ChatHandler.register(user, sid)
        return user.json()

    # retrieve chat history
    # request data json:
    # {
    #     "jwt_token": "USER-JWT-TOKEN",
    #     "to_user": 1,
    #     "page": 1,
    #     "limit": 20,
    #     "sort": 1,
    #     "order_by": "send_date",
    #     "search": null,
    # }
    def on_chat_list(self, data):
        user = ChatHandler.auth_user(data)

        opts_dict: Dict[Any, Any] = {}
        opts_dict["page"] = int(data["page"])
        opts_dict["limit"] = int(data["limit"])
        opts_dict["sort"] = int(data["sort"])
        opts_dict["order_by"] = data["order_by"]
        opts_dict["from_user_id"] = int(user.id)
        opts_dict["to_user_id"] = int(data["to_user"])
        if hasattr(data, "search"):
            opts_dict["search"] = data["search"]

        vobj = validate_object(ChatHistoryPaginationOptions, opts_dict)

        opts = ChatHistoryPaginationOptions()
        opts.page = int(vobj.page)
        opts.limit = int(vobj.limit)
        opts.sort = int_to_sort(int(vobj.sort))
        opts.order_by = vobj.order_by
        opts.from_user_id = int(vobj.from_user_id)
        opts.to_user_id = int(vobj.to_user_id)
        if hasattr(vobj, "search"):
            opts.search = vobj.search
        else:
            opts.search = ""

        chat_history = ChatService.list_chat_history(opts)

        response = []
        for chat in chat_history:
            response.append(chat.json())

        return response

    def on_chat_send(self, data):
        user = ChatHandler.auth_user(data)
        to_user_id = data["to_user"]
        message = data["message"]

        from_user = UserService.find_by_id(user.id)
        to_user = UserService.find_by_id(to_user_id)

        ChatService.send_chat(from_user, to_user, message)

        # send to self
        ChatHandler.emit(
            user,
            "chat_receive",
            {
                "chat_from_user_id": from_user.id,
                "chat_to_user_id": to_user.id,
                "chat_message": message,
            },
        )

        # send to target user
        try:
            ChatHandler.emit(
                to_user,
                "chat_receive",
                {
                    "chat_from_user_id": from_user.id,
                    "chat_to_user_id": to_user.id,
                    "chat_message": message,
                },
            )
        except:
            ChatHandler.emit(
                user,
                "chat_receive",
                {
                    "chat_from_system": True,
                    "chat_message": "Target user is offline!",
                },
            )

        # update chat head
        ChatService.update_chat_head(to_user, from_user)

        # return true
        return True
