"""
    chat service
"""

from typing import List

from database.database import db_session
from sqlalchemy import text
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import and_, or_
from user.model import User
from werkzeug.exceptions import InternalServerError

from chat.model import Chat


class ChatService:
    @staticmethod
    def send_chat(from_user: User, to_user: User, message: str):
        try:
            chat_message = Chat(from_user.id, to_user.id, message)
            db_session.add(chat_message)
            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to send chat!")

    @staticmethod
    def list_chat_history(from_user: User, to_user: User) -> List[Chat]:
        try:
            chat_history: Query = Chat.query.where(
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
            chat_history = chat_history.order_by(text("id DESC")).limit(10)
            chat_history = Chat.query.select_from(chat_history).order_by(text("id ASC"))
            chat_history = chat_history.all()
            return chat_history
        except Exception as e:
            print(e)
            raise InternalServerError("Failed to retrieve chat history!")
