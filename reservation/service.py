from datetime import datetime
from typing import List

from car.model import Car
from car.service import CarService
from database.database import db_session
from pagination.pagination import Pagination, PaginationOptions
from parking_lot.model import ParkingLot
from parking_lot.service import ParkingLotService
from sqlalchemy import and_, or_
from user.model import User
from user.service import UserService
from werkzeug.exceptions import Conflict, Forbidden, NotFound

from reservation.model import Reservation


class ReservationPaginationResult:
    def __init__(self, raw):
        self.reservation: Reservation = raw[0]
        self.user: User = raw[1]
        self.car: Car = raw[2]

    def json(self):
        return {
            "reservation": self.reservation.json(),
            "user": self.user.json_shareable(),
            "car": self.car.json(),
        }


class ReservationService:
    @staticmethod
    def create_reservation(
        user: User,
        car: Car,
        parking_lot: ParkingLot,
        start_time: datetime,
    ):
        try:
            # create reservation
            reservation = Reservation(user.id, car.id, parking_lot.id, start_time)
            # validate reservation
            ReservationService.validate_reservation(reservation)
            # commit to database
            db_session.add(reservation)
            db_session.commit()
            # return created reservation
            return reservation
        except Exception as err:
            db_session.rollback()
            print(err)
            raise err

    @staticmethod
    def end_reservation(reservation: Reservation, end_time=datetime.utcnow()) -> None:
        db_session.query(Reservation).filter(Reservation.id == reservation.id).update(
            {"end_time": end_time}
        )
        db_session.commit()

    @staticmethod
    def validate_reservation(reservation: Reservation):
        # check is user valid
        user = UserService.find_by_id(reservation.user_id)
        if user == None:
            raise NotFound("User not found!")

        # check is car valid
        car = CarService.find_by_id(reservation.car_id)
        if car == None:
            raise NotFound(f"Car #{reservation.car_id} not found!")

        # check is car already park
        is_car_parking = CarService.is_car_parking(car)
        if is_car_parking == True:
            raise Forbidden(f"Car #{car.id} already parking!")

        # check is user own this car
        user_own_car = car.car_owner_id == user.id
        if user_own_car == False:
            raise Forbidden("User not owning the car!")

        # check is parking lot valid
        parking_lot = ParkingLotService.find_by_id(reservation.parking_lot_id)
        if parking_lot == None:
            raise NotFound(f"Parking lot #{parking_lot.id} not found!")

        # check is parking lot available
        parking_lot_available = ParkingLotService.is_parking_lot_available(parking_lot)
        if parking_lot_available == False:
            raise Conflict(f"Parking lot #{parking_lot.id} not available!")

        # successful validation
        return True

    @staticmethod
    def find_by_id(id: int) -> Reservation:
        return Reservation.query.filter(Reservation.id == id).first()

    @staticmethod
    def get_user_reservation(
        user: User, options: PaginationOptions
    ) -> List[Reservation]:
        query = (
            db_session.query(Reservation, User, Car)
            .join(User, User.id == Reservation.user_id)
            .join(Car, Car.id == Reservation.car_id)
            .where(
                and_(
                    or_(
                        # find by id
                        Reservation.id.ilike(f"%{options.search}%"),
                        # find by user
                        User.id.ilike(f"%{options.search}%"),
                        User.email.ilike(f"%{options.search}%"),
                        User.username.ilike(f"%{options.search}%"),
                        User.firstname.ilike(f"%{options.search}%"),
                        User.lastname.ilike(f"%{options.search}%"),
                        User.phone_number.ilike(f"%{options.search}%"),
                        User.citizen_id.ilike(f"%{options.search}%"),
                        # find by car
                        Car.car_license_plate.ilike(f"%{options.search}%"),
                        Car.car_type.ilike(f"%{options.search}%"),
                    ),
                    User.id == user.id,
                )
            )
        )
        pagination = Pagination(Reservation, query)
        pagination.set_options(options)
        result = pagination.result()

        response = []

        for raw in result:
            new_obj = ReservationPaginationResult(raw)
            response.append(new_obj.json())

        return response

    @staticmethod
    def admin_pagination_reservation(
        options: PaginationOptions,
    ) -> List[ReservationPaginationResult]:
        query = (
            db_session.query(Reservation, User, Car)
            .join(User, User.id == Reservation.user_id)
            .join(Car, Car.id == Reservation.car_id)
            .where(
                or_(
                    # find by id
                    Reservation.id.ilike(f"%{options.search}%"),
                    # find by user
                    User.id.ilike(f"%{options.search}%"),
                    User.email.ilike(f"%{options.search}%"),
                    User.username.ilike(f"%{options.search}%"),
                    User.firstname.ilike(f"%{options.search}%"),
                    User.lastname.ilike(f"%{options.search}%"),
                    User.phone_number.ilike(f"%{options.search}%"),
                    User.citizen_id.ilike(f"%{options.search}%"),
                    # find by car
                    Car.car_license_plate.ilike(f"%{options.search}%"),
                    Car.car_type.ilike(f"%{options.search}%"),
                )
            )
        )
        pagination = Pagination(Reservation, query)
        pagination.set_options(options)
        result = pagination.result()

        response = []

        for raw in result:
            new_obj = ReservationPaginationResult(raw)
            response.append(new_obj.json())

        return response
