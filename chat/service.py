"""
    chat service
"""

from datetime import datetime
from typing import List

from database.database import db_session
from marshmallow import fields, validate
from pagination.pagination import Pagination, PaginationOptions, PaginationSortOptions
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import and_, or_
from user.model import User
from user.service import UserService
from werkzeug.exceptions import InternalServerError

from chat.model import Chat, ChatHead


class ChatHistoryPaginationOptions(PaginationOptions):
    from_user_id = fields.Integer(required=True, validate=validate.Range(min=1))
    to_user_id = fields.Integer(required=True, validate=validate.Range(min=1))


class ChatService:
    @staticmethod
    def send_chat(
        from_user: User, to_user: User, message: str, update_target_chat_head=True
    ):
        success = False
        try:
            chat_message = Chat(from_user.id, to_user.id, message)
            db_session.add(chat_message)
            db_session.commit()
            success = True
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to send chat!")

        if success == True and update_target_chat_head == True:
            ChatService.update_chat_head(to_user, from_user)

    @staticmethod
    def list_chat_history(opts: ChatHistoryPaginationOptions) -> List[Chat]:
        try:
            from_user = UserService.find_by_id(opts.from_user_id)
            to_user = UserService.find_by_id(opts.to_user_id)

            query: Query = db_session.query(Chat)
            query = query.where(
                or_(
                    (
                        and_(
                            Chat.from_user_id == from_user.id,
                            Chat.to_user_id == to_user.id,
                        )
                    ),
                    (
                        and_(
                            Chat.from_user_id == to_user.id,
                            Chat.to_user_id == from_user.id,
                        )
                    ),
                )
            )

            pagination = Pagination(Chat, query)
            pagination.set_options(opts)
            result = pagination.result()

            return result
        except Exception as e:
            print(e)
            raise InternalServerError("Failed to retrieve chat history!")

    @staticmethod
    def update_chat_head(user: User, from_user: User):
        try:
            exists_chat_head: Query = ChatHead.query.where(
                and_(
                    ChatHead.user_id == user.id, ChatHead.target_user_id == from_user.id
                )
            )
            exists_chat_head = exists_chat_head.first()

            if exists_chat_head != None:
                db_session.query(ChatHead).filter(
                    ChatHead.id == exists_chat_head.id
                ).update({"last_update_date": datetime.now()})
            else:
                new_chat_head = ChatHead(user.id, from_user.id, datetime.now())
                db_session.add(new_chat_head)

            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to update chat head!")

    @staticmethod
    def list_chat_head(
        user: User, pagination_options: PaginationOptions
    ) -> List[ChatHead]:
        chat_heads_query = ChatHead.query.where(ChatHead.user_id == user.id)
        pagination = Pagination(ChatHead, chat_heads_query)
        pagination_options.sort = PaginationSortOptions.DESC
        pagination_options.order_by = "last_update_date"
        pagination.set_options(pagination_options)
        result = pagination.result()
        return result
