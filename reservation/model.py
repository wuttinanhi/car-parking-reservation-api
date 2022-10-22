import datetime

from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"))
    car_id = Column(Integer(), ForeignKey("cars.id"))
    parking_lot_id = Column(Integer(), ForeignKey("parking_lots.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)

    def __init__(
        self, user_id: int, car_id: int, parking_lot_id: int, start_time: datetime
    ):
        self.user_id = user_id
        self.car_id = car_id
        self.parking_lot_id = parking_lot_id
        self.start_time = start_time

    def __repr__(self):
        return f"<Reservation {self.id}>"

    def json(self):
        return {
            "reservation_id": self.id,
            "reservation_start_time": self.start_time,
            "reservation_end_time": self.end_time,
        }
