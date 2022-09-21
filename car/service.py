from typing import List

from database.database import db_session
from sqlalchemy.exc import IntegrityError
from user.model import User
from werkzeug.exceptions import Conflict

from car.model import Car


class CarService:
    @staticmethod
    def add(car_owner: User, car_license_plate: str, car_type: str):
        try:
            car = Car(car_license_plate, car_owner.id, car_type)
            db_session.add(car)
            db_session.commit()
            return car
        except IntegrityError:
            db_session.rollback()
            raise Conflict("Car already registerd!")

    @staticmethod
    def remove(car: Car):
        db_session.delete(car)
        db_session.commit()

    @staticmethod
    def find_by_license_plate(car_license_plate: str):
        return Car.query.filter(Car.car_license_plate == car_license_plate).first()

    @staticmethod
    def find_all_car_by_user(user: User):
        return Car.query.filter(Car.car_owner_id == user.id).all()

    @staticmethod
    def find_by_id(id: int) -> Car:
        return Car.query.filter(Car.id == id).first()

    @staticmethod
    def is_user_own_car(user: User, car: Car):
        return car.car_owner_id == user.id

    @staticmethod
    def get_all_cars_by_user(user: User) -> List[Car]:
        return Car.query.filter(Car.car_owner_id == user.id).all()
