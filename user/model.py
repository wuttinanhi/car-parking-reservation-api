"""
    user model
"""

from database.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email!r}>'
