"""
    user model
"""

from database.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String(50), unique=True)
    password = Column(String(100))

    username = Column(String(30), unique=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    phone_number = Column(String(10))
    citizen_id = Column(String(13))

    def __init__(
        self,
        email: str,
        password: str,
        username: str,
        firstname: str,
        lastname: str,
        phone_number: str,
        citizen_id: str,
    ):
        self.email = email
        self.password = password
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number
        self.citizen_id = citizen_id

    def __repr__(self):
        return f"<User {self.username}>"

    def json(self):
        return {
            "user_id": self.id,
            "user_username": self.username,
        }

    def json_shareable(self):
        return {
            "user_id": self.id,
            "user_email": self.email,
            "user_username": self.username,
            "user_firstname": self.firstname,
            "user_lastname": self.lastname,
            "user_phone_number": self.phone_number,
        }

    def json_full(self):
        return {
            "user_id": self.id,
            "user_email": self.email,
            "user_username": self.username,
            "user_firstname": self.firstname,
            "user_lastname": self.lastname,
            "user_phone_number": self.phone_number,
            "user_citizen_id": self.citizen_id,
        }
