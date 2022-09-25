'''
    auth blueprint
'''


from http.client import CREATED, FORBIDDEN, NOT_FOUND, OK

from auth.decorator import admin_only, login_required
from flask import Blueprint, request
from marshmallow import Schema, fields, validate
from util.validate_request import ValidateRequest

from parking_lot.service import ParkingLotService

blueprint = Blueprint("parking_lot", __name__, url_prefix="/parking_lot")


class ParkingLotAddDto(Schema):
    location = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    open_status = fields.Boolean(required=True)


class ParkingLotDeleteDto(Schema):
    parking_lot_id = fields.Int(required=True)


@blueprint.route('/add', methods=['POST'])
@admin_only
def add_parking_lot():
    data = ValidateRequest(ParkingLotAddDto, request)
    ParkingLotService.add(data.location, data.open_status)
    return {"message": "Parking lot added."}, CREATED


@blueprint.route('/remove', methods=['DELETE'])
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


@blueprint.route('/available', methods=['GET'])
@login_required
def all_parking_lot():
    response = []
    parking_lots = ParkingLotService.get_all_parking_lot_with_available_status()
    for row in parking_lots:
        response.append({
            'id': row['id'],
            'location': row["location"],
            'open_status': row["open_status"],
            'available': row["available"]
        })
    return response
