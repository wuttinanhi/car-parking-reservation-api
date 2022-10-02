from bcrypt_wrapper.service import BcryptService
from database.database import db_session
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict

from user import User


class UserService:
    @staticmethod
    def register(
        email: str,
        password: str,
        username: str,
        firstname: str,
        lastname: str,
        phone_number: str,
    ):
        try:
            hashed_password = BcryptService.hash(password)
            user = User(
                email, hashed_password, username, firstname, lastname, phone_number
            )
            db_session.add(user)
            db_session.commit()
            return user
        except IntegrityError:
            db_session.rollback()
            raise Conflict("User already registerd!")

    @staticmethod
    def login(email: str, password: str):
        user: User = UserService.find_by_email(email)
        if user:
            check_pwd = BcryptService.validate(password, user.password)
            return check_pwd
        return False

    @staticmethod
    def find_by_email(email: str):
        user: User = User.query.filter(User.email == email).first()
        return user

    @staticmethod
    def find_by_id(id: int):
        user: User = User.query.filter(User.id == id).first()
        return user
