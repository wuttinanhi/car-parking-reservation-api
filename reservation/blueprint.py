"""
    auth blueprint
"""


from datetime import datetime
from http.client import CONFLICT, CREATED, FORBIDDEN, NOT_FOUND, OK

from auth.decorator import admin_only, login_required
from auth.function import get_user
from car.service import CarService
from flask import Blueprint, request
from marshmallow import Schema, fields
from pagination.pagination import create_pagination_options_from_request
from payment.service import PaymentService
from util.validate_request import validate_request

from reservation.service import ParkingLotService, ReservationService

blueprint = Blueprint("reservation", __name__, url_prefix="/reservation")


class ReservationCreateDto(Schema):
    car_id = fields.Int(required=True)
    parking_lot_id = fields.Int(required=True)


class ReservationEndDto(Schema):
    reservation_id = fields.Int(required=True)


class ReservationAdminEndDto(ReservationEndDto):
    create_invoice = fields.Boolean(required=True)


@blueprint.route("/create", methods=["POST"])
@login_required
def create_reservation():
    user = get_user()
    data = validate_request(ReservationCreateDto, request)
    car = CarService.find_by_id(data.car_id)
    parking_lot = ParkingLotService.find_by_id(data.parking_lot_id)
    ReservationService.create_reservation(user, car, parking_lot, datetime.utcnow())
    return {"message": "Reservation created."}, CREATED


@blueprint.route("/end", methods=["DELETE"])
@login_required
def end_reservation():
    # get user
    user = get_user()
    # validate request
    data = validate_request(ReservationEndDto, request)
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

        # create invoice
        PaymentService.create_invoice(reservation)

        # return success response
        return {"message": "Reservation ended."}, OK

    # reservation not found
    return {"error": "Reservation not found!"}, NOT_FOUND


@blueprint.route("/admin/end", methods=["DELETE"])
@admin_only
def admin_end_reservation():
    # validate request
    data = validate_request(ReservationAdminEndDto, request)
    # get reservation
    reservation = ReservationService.find_by_id(data.reservation_id)

    # check is reservation exists
    if reservation:
        # check is reservation already end
        if reservation.end_time:
            return {"error": "Reservation already end!"}, CONFLICT

        # end reservation
        ReservationService.end_reservation(reservation)

        # create invoice
        if data.create_invoice is True:
            PaymentService.create_invoice(reservation)

        # return success response
        return {"message": "Reservation ended."}, OK

    # reservation not found
    return {"error": "Reservation not found!"}, NOT_FOUND


@blueprint.route("/list", methods=["GET"])
@login_required
def user_reservation():
    user = get_user()
    pagination_options = create_pagination_options_from_request(request)
    result = ReservationService.pagination_reservation(pagination_options, user)
    return result


@blueprint.route("/admin/list", methods=["GET"])
@admin_only
def admin_pagination_reservation():
    pagination_options = create_pagination_options_from_request(request)
    result = ReservationService.pagination_reservation(pagination_options)
    return result
