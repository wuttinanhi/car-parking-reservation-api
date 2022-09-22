'''
    auth blueprint
'''


from http.client import (BAD_REQUEST, CREATED, INTERNAL_SERVER_ERROR,
                         NOT_FOUND, OK, HTTPException)

from auth.decorator import login_required
from flask import Blueprint, request
from marshmallow import Schema, ValidationError, fields, validate
from util.validate_request import ValidateRequest
from werkzeug.exceptions import HTTPException

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
@login_required
def add_parking_lot():
    data = ValidateRequest(ParkingLotAddDto, request)
    ParkingLotService.add(data.location, data.open_status)
    return {"message": "Parking lot added."}, CREATED


@blueprint.route('/remove', methods=['DELETE'])
@login_required
def remove_parking_lot():
    data = ValidateRequest(ParkingLotDeleteDto, request)
    parking_lot = ParkingLotService.find_by_id(data.parking_lot_id)
    if parking_lot:
        ParkingLotService.remove(parking_lot)
        return {"message": "Parking lot deleted."}, OK
    return {"error": "Parking lot not found!"}, NOT_FOUND


@blueprint.route('/all', methods=['GET'])
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


@blueprint.errorhandler(Exception)
def error_handle(err: Exception):
    if issubclass(type(err), ValidationError):
        return str(err), BAD_REQUEST
    if issubclass(type(err), HTTPException):
        return {'error': err.description}, err.code
    return {'error': "Internal server exception!"}, INTERNAL_SERVER_ERROR
