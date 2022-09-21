"""
    mock class
"""

from datetime import datetime

from car.service import CarService
from database.database import Base, db_session, engine, init_db
from parking_lot.service import ParkingLotService
from reservation.service import ReservationService
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
        car_a = CarService.add(user, "A11111", "Tesla")
        car_b = CarService.add(user, "A22222", "Starship")

        # get all car
        # user_cars = CarService.find_all_car_by_user(user)
        # for car in user_cars:
        #     print(car)

        # mock parking lot
        parking_lot_1 = ParkingLotService.add("Floor 1", True)
        parking_lot_2 = ParkingLotService.add("Floor 2", True)
        parking_lot_3 = ParkingLotService.add("Floor 3", False)

        # mock reservation
        reservation_1 = ReservationService.create_reservation(
            user, car_a, parking_lot_1, datetime.utcnow())

        # end created reservation
        ReservationService.end_reservation(reservation_1)

        # remove database session
        db_session.remove()
