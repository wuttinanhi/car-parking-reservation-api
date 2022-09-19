from database import Base
from sqlalchemy import Column, Integer, String


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
