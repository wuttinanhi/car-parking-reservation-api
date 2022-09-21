"""
    mock class
"""

from car.service import CarService
from database.database import Base, db_session, engine, init_db
from parking_lot.service import ParkingLotService
from user.service import UserService


class Mock:
    # drop all
    @staticmethod
    def clean_db():
        Base.metadata.drop_all(bind=engine)

    # setup database
    @staticmethod
    def setup_db():
        init_db()

    @staticmethod
    def mock():
        # mock user
        UserService.register("test@example.com", "@Test12345")

        # get user
        user = UserService.find_by_email("test@example.com")

        # mock user car
        CarService.add(user, "A11111", "Tesla")
        CarService.add(user, "A22222", "Starship")

        # get all car
        user_cars = CarService.find_all_car_by_user(user)
        for car in user_cars:
            print(car)

        # mock parking lot
        ParkingLotService.add("Floor 1", True)
        ParkingLotService.add("Floor 2", True)
        ParkingLotService.add("Floor 3", False)

        # remove database session
        db_session.remove()
