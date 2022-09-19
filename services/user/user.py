from services.bcrypt_wrapper.bcrypt_wrapper import BcryptWrapper
from services.database import Base, db_session
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError


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


class UserService:
    @staticmethod
    def register(email: str, password: str):
        try:
            hashed_password = BcryptWrapper.hash(password)
            user = User(email, hashed_password)
            db_session.add(user)
            db_session.commit()
            return user
        except IntegrityError:
            db_session.rollback()
            raise Exception("User already registerd!")

    @staticmethod
    def login(email: str, password: str):
        user: User = UserService.find_by_email(email)
        if user:
            check_pwd = BcryptWrapper.validate(password, user.password)
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
