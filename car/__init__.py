"""
    car module
"""

from car.blueprint import blueprint as car_blueprint
from car.model import Car
from car.service import CarService

__all__ = [Car, car_blueprint, CarService]
