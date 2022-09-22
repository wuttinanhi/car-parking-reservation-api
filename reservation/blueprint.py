'''
    auth blueprint
'''


from datetime import datetime
from http.client import CONFLICT, CREATED, FORBIDDEN, NOT_FOUND, OK

from auth.decorator import login_required
from auth.function import GetUser
from car.service import CarService
from flask import Blueprint, request
from marshmallow import Schema, fields
from util.validate_request import ValidateRequest

from reservation.service import ParkingLotService, ReservationService

blueprint = Blueprint("reservation", __name__, url_prefix="/reservation")


class ReservationCreateDto(Schema):
    car_id = fields.Int(required=True)
    parking_lot_id = fields.Int(required=True)


class ReservationEndDto(Schema):
    reservation_id = fields.Int(required=True)


@blueprint.route('/create', methods=['POST'])
@login_required
def create_reservation():
    user = GetUser()
    data = ValidateRequest(ReservationCreateDto, request)
    car = CarService.find_by_id(data.car_id)
    parking_lot = ParkingLotService.find_by_id(data.parking_lot_id)
    ReservationService.create_reservation(
        user,
        car,
        parking_lot,
        datetime.utcnow()
    )
    return {"message": "Reservation created."}, CREATED


@blueprint.route('/end', methods=['DELETE'])
@login_required
def end_reservation():
    # get user
    user = GetUser()
    # validate request
    data = ValidateRequest(ReservationEndDto, request)
    # get reservation
    reservation = ReservationService.find_by_id(data.reservation_id)

    # check is reservation exists
    if reservation:
        # check is user own reservation
        if reservation.user_id != user.id:
            return {"error": "User not own reservation"}, FORBIDDEN

        # check is reservation already end
        if reservation.end_time:
            return {"error": "Reservation already end!"}, CONFLICT

        # end reservation
        ReservationService.end_reservation(reservation)
        return {"message": "Reservation ended."}, OK

    # reservation not found
    return {"error": "Reservation not found!"}, NOT_FOUND


@blueprint.route('/user_reservation', methods=['GET'])
@login_required
def user_reservation():
    user = GetUser()
    response = []
    all_reservations = ReservationService.get_user_reservation(user)
    for car in all_reservations:
        response.append(car.json())
    return response
