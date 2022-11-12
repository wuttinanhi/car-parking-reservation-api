from datetime import datetime
from typing import List

from flask import current_app
from sqlalchemy import or_
from sqlalchemy.orm import Query
from werkzeug.exceptions import Conflict, Forbidden, NotFound

from car.model import Car
from car.service import CarService
from database.database import db_session
from pagination.pagination import Pagination, PaginationOptions
from parking_lot.model import ParkingLot
from parking_lot.service import ParkingLotService
from reservation.model import Reservation
from user.model import User
from user.service import UserService


class ReservationPaginationResult:
    def __init__(self, raw):
        self.reservation: Reservation = raw[0] or None
        self.user: User = raw[1] or None
        self.car: Car = raw[2] or None
        self.parking_lot: ParkingLot = raw[3] or None

    def json(self):
        return {
            "reservation": self.reservation.json()
            if self.reservation is not None
            else None,
            "user": self.user.json_shareable() if self.user is not None else None,
            "car": self.car.json() if self.car is not None else None,
            "parking_lot": self.parking_lot.json()
            if self.parking_lot is not None
            else None,
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
            current_app.logger.error(err)
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
    def pagination_reservation(
        options: PaginationOptions, user: User = None
    ) -> List[ReservationPaginationResult]:
        query: Query = db_session.query(Reservation, User, Car, ParkingLot)
        query = (
            query.join(User, User.id == Reservation.user_id, isouter=True)
            .join(Car, Car.id == Reservation.car_id, isouter=True)
            .join(ParkingLot, ParkingLot.id == Reservation.parking_lot_id, isouter=True)
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

        if user is not None:
            query = query.filter(Reservation.user_id == user.id)

        pagination = Pagination(Reservation, query)
        pagination.set_options(options)
        result = pagination.result()

        response = []

        for raw in result:
            new_obj = ReservationPaginationResult(raw)
            response.append(new_obj.json())

        return response
