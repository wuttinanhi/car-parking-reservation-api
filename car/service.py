from database.database import db_session
from sqlalchemy.exc import IntegrityError
from user.model import User
from werkzeug.exceptions import Conflict, InternalServerError, NotFound

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
    def find_by_license_plate(car_license_plate: str) -> Car:
        car = Car.query.filter(Car.car_license_plate == car_license_plate).first()
        if car == None:
            raise NotFound("Car not found!")
        return car

    @staticmethod
    def find_all_car_by_user(user: User)-> Car:
        return Car.query.filter(Car.car_owner_id == user.id).all()

    @staticmethod
    def find_by_id(id: int) -> Car:
        car = Car.query.filter(Car.id == id).first()
        if car == None:
            raise NotFound("Car not found!")
        return car

    @staticmethod
    def is_user_own_car(user: User, car: Car):
        return car.car_owner_id == user.id

    @staticmethod
    def is_car_parking(car: Car):
        result = db_session.execute(
            """
                # check parking car

                SELECT 
                    *
                FROM
                    reservations
                LEFT JOIN
                    cars
                ON
                    reservations.car_id = cars.id
                WHERE
                    reservations.end_time IS NULL
                    AND
                    cars.id = :car_id
            """,
            {"car_id": car.id},
        )
        return len(result.all()) >= 1

    @staticmethod
    def update(car: Car):
        try:
            Car.query.filter(Car.id == car.id).update(
                {
                    "car_license_plate": car.car_license_plate,
                    "car_type": car.car_type,
                }
            )
            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to update user!")
