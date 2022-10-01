"""
    chat model
"""

from database import Base
from sqlalchemy import Column, Integer, String


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer(), primary_key=True)
    from_user_id = Column(Integer(), nullable=False)
    to_user_id = Column(Integer(), nullable=False)
    message = Column(String(255), nullable=False)

    def __init__(self, from_user_id: int, to_user_id: int, message: str):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message

    def __repr__(self):
        return f"<Chat {self.id}>"

    def json(self):
        return {
            "chat_id": self.id,
            "chat_from_user_id": self.from_user_id,
            "chat_to_user_id": self.to_user_id,
            "chat_message": self.message,
        }
