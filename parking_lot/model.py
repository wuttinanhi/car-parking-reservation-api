from database import Base
from sqlalchemy import Boolean, Column, Integer, String


class ParkingLot(Base):
    __tablename__ = 'parking_lots'

    id = Column(Integer, primary_key=True)
    location = Column(String(100))
    open_status = Column(Boolean, default=False, nullable=False)

    def __init__(self, location: str, open_status: bool):
        self.location = location
        self.open_status = open_status

    def __repr__(self):
        return f'<ParkingLot {self.id}>'

    def json(self):
        return {
            'parking_lot_id': self.id,
            'parking_lot_location': self.location,
            'parking_lot_open_status': self.open_status
        }
