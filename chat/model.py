"""
    chat model
"""

from datetime import datetime

from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from user.service import UserService


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer(), primary_key=True)
    from_user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    send_date = Column(DateTime(), nullable=False)

    def __init__(
        self,
        from_user_id: int,
        to_user_id: int,
        message: str,
        send_date=datetime.now(),
    ):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message
        self.send_date = send_date

    def __repr__(self):
        return f"<Chat id={self.id} from_user_id={self.from_user_id} to_user_id={self.to_user_id} send_date={self.send_date} message={self.message!r}>"

    def json(self):
        return {
            "chat_id": self.id,
            "chat_from_user_id": self.from_user_id,
            "chat_to_user_id": self.to_user_id,
            "chat_send_date": str(self.send_date),
            "chat_message": self.message,
        }


class ChatHead(Base):
    __tablename__ = "chat_heads"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    target_user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    last_update_date = Column(DateTime(), nullable=False)

    def __init__(self, user_id: int, target_user_id: int, last_update=datetime.now()):
        self.user_id = user_id
        self.target_user_id = target_user_id
        self.last_update_date = last_update

    def __repr__(self):
        return f"<ChatHead id={self.id} user_id={self.user_id} target_user_id={self.target_user_id} last_update={self.last_update_date}>"

    def json(self):
        return {
            "chat_head_id": self.id,
            "chat_head_user_id": self.user_id,
            "chat_head_target_user_id": self.target_user_id,
            "chat_head_last_update_date": str(self.last_update_date),
        }

    def json_populated(self):
        return {
            "chat_head_id": self.id,
            "chat_head_user_id": self.user_id,
            "chat_head_target_user_id": self.target_user_id,
            "chat_head_target_user": UserService.find_by_id(self.target_user_id).json(),
            "chat_head_last_update_date": str(self.last_update_date),
        }
