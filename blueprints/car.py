'''
    auth blueprint
'''


from http.client import BAD_REQUEST, CREATED, FORBIDDEN, NOT_FOUND, OK
from xmlrpc.client import INTERNAL_ERROR

from flask import Blueprint, request
from marshmallow import Schema, ValidationError, fields, validate
from services.auth.decorator import login_required
from services.auth.function import GetUser
from services.car.car import CarService
from util.validate_request import ValidateRequest

bp = Blueprint("car", __name__, url_prefix="/car")


class CarAddDto(Schema):
    car_license_plate = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=10)
    )
    car_type = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=10)
    )


class CarDeleteDto(Schema):
    car_id = fields.Int(required=True)


@bp.route('/add', methods=['POST'])
@login_required
def add_car():
    user = GetUser()
    data = ValidateRequest(CarAddDto, request)
    CarService.add(user, data.car_license_plate, data.car_type)
    return {"message": "Car add."}, CREATED


@bp.route('/remove', methods=['DELETE'])
@login_required
def remove_car():
    user = GetUser()
    data = ValidateRequest(CarDeleteDto, request)
    car = CarService.find_by_id(data.car_id)
    if car:
        car_owner_check = CarService.is_user_own_car(user, car)
        if car_owner_check == True:
            CarService.remove(car)
            return {"message": "Car delete."}, OK
        return {"error": "Forbidden"}, FORBIDDEN
    return {"message": "Car not found!"}, NOT_FOUND


@bp.errorhandler(Exception)
def error_handle(err: Exception):
    if err.__class__ is ValidationError:
        return str(err), BAD_REQUEST
    return {'message': "Internal server exception!", "error": str(err)}, INTERNAL_ERROR
