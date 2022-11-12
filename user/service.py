from typing import List

from flask import current_app
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict, InternalServerError

from bcrypt_wrapper.service import BcryptService
from database.database import db_session
from pagination.pagination import Pagination, PaginationOptions
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
        citizen_id: str,
    ):
        try:
            hashed_password = BcryptService.hash(password)
            user = User(
                email,
                hashed_password,
                username,
                firstname,
                lastname,
                phone_number,
                citizen_id,
            )
            db_session.add(user)
            db_session.commit()
            return user
        except IntegrityError:
            db_session.rollback()
            raise Conflict("User already registerd!")

    @staticmethod
    def compare_password(user: User, password: str):
        return BcryptService.validate(password, user.password)

    @staticmethod
    def login(email: str, password: str):
        user: User = UserService.find_by_email(email)
        if user:
            check_pwd = UserService.compare_password(user, password)
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

    @staticmethod
    def paginate_user(options: PaginationOptions) -> List[User]:
        search_value = options.search
        query = User.query.where(
            or_(
                User.email.like(f"%{search_value}%"),
                User.username.like(f"%{search_value}%"),
                User.firstname.like(f"%{search_value}%"),
                User.lastname.like(f"%{search_value}%"),
                User.phone_number.like(f"%{search_value}%"),
                User.citizen_id.like(f"%{search_value}%"),
            )
        )

        pagination = Pagination(User, query)
        pagination.set_options(options)
        return pagination.result()

    @staticmethod
    def update(user: User):
        try:
            User.query.filter(User.id == user.id).update(
                {
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "phone_number": user.phone_number,
                    "citizen_id": user.citizen_id,
                }
            )
            db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db_session.rollback()
            raise InternalServerError("Failed to update user!")

    @staticmethod
    def change_password(user: User, password: str):
        try:
            new_hashed_password = BcryptService.hash(password)
            User.query.filter(User.id == user.id).update(
                {"password": new_hashed_password}
            )
            db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db_session.rollback()
            raise InternalServerError("Failed to change user password!")
