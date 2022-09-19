from services.database import Base, db_session
from services.user.user import User
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    car_license_plate = Column(String(100), unique=True)
    car_owner_id = Column(Integer())
    car_type = Column(String(100))

    def __init__(self, car_license_plate: str, car_owner_id: str, car_type: str):
        self.car_license_plate = car_license_plate
        self.car_owner_id = car_owner_id
        self.car_type = car_type

    def __repr__(self):
        return f'<Car {self.id}>'


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
            raise Exception("Car already registerd!")

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
    def find_by_id(id: int):
        return Car.query.filter(Car.id == id).first()

    @staticmethod
    def is_user_own_car(user: User, car: Car):
        return car.car_owner_id == user.id
