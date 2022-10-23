"""
    auth blueprint
"""


from http.client import CREATED, FORBIDDEN, NOT_FOUND, OK

from auth.decorator import admin_only, login_required
from flask import Blueprint, request
from marshmallow import Schema, fields, validate
from util.validate_request import ValidateRequest

from parking_lot.service import ParkingLotService

blueprint = Blueprint("parking_lot", __name__, url_prefix="/parking_lot")


class ParkingLotAddDto(Schema):
    location = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    open_status = fields.Boolean(required=True)


class ParkingLotUpdateDto(ParkingLotAddDto):
    parking_lot_id = fields.Int(required=True)


class ParkingLotDeleteDto(Schema):
    parking_lot_id = fields.Int(required=True)


@blueprint.route("/admin/add", methods=["POST"])
@admin_only
def add_parking_lot():
    data = ValidateRequest(ParkingLotAddDto, request)
    ParkingLotService.add(data.location, data.open_status)
    return {"message": "Parking lot added."}, CREATED


@blueprint.route("/admin/remove", methods=["DELETE"])
@admin_only
def remove_parking_lot():
    data = ValidateRequest(ParkingLotDeleteDto, request)
    parking_lot = ParkingLotService.find_by_id(data.parking_lot_id)

    # check is parking lot none
    if parking_lot == None:
        return {"error": "Parking lot not found!"}, NOT_FOUND

    # check parking lot valid for delete
    is_available = ParkingLotService.is_parking_lot_available(parking_lot)
    if is_available == False:
        return {"error": "Parking lot busy!"}, FORBIDDEN

    ParkingLotService.remove(parking_lot)
    return {"message": "Parking lot deleted."}, OK


@blueprint.route("/admin/update", methods=["PATCH"])
@admin_only
def update_parking_lot():
    data = ValidateRequest(ParkingLotUpdateDto, request)
    parking_lot = ParkingLotService.find_by_id(data.parking_lot_id)

    parking_lot.location = data.location
    parking_lot.open_status = data.open_status

    ParkingLotService.update(parking_lot)
    return {"message": "Successfully updated parking lot."}, 200


@blueprint.route("/admin/available", methods=["GET"])
@admin_only
def admin_available_parking_lot():
    response = []
    parking_lots = ParkingLotService.get_all_parking_lot_with_available_status()
    for obj in parking_lots:
        response.append(obj.json())
    return response


@blueprint.route("/available", methods=["GET"])
@login_required
def available_parking_lot():
    response = []
    parking_lots = ParkingLotService.get_all_parking_lot_with_available_status()
    for obj in parking_lots:
        response.append(obj.json())
    return response
