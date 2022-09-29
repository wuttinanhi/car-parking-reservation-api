"""
    settings model
"""
from database import Base
from sqlalchemy import Column, Float, Integer


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    charge_within_hour = Column(Float)
    charge_more_than_a_hour = Column(Float)
    charge_more_than_a_day = Column(Float)

    def __init__(
        self,
        charge_within_hour: float,
        charge_more_than_a_hour: float,
        charge_more_than_a_day: float
    ):
        self.charge_within_hour = charge_within_hour
        self.charge_more_than_a_hour = charge_more_than_a_hour
        self.charge_more_than_a_day = charge_more_than_a_day

    def __repr__(self):
        return f'<Setting {self.id}>'

    def json(self):
        return {
            'charge_within_hour': self.charge_within_hour,
            'charge_more_than_a_hour': self.charge_more_than_a_hour,
            'charge_more_than_a_day': self.charge_more_than_a_day
        }
