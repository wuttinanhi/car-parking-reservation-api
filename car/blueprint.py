'''
    auth blueprint
'''


from http.client import (BAD_REQUEST, CREATED, FORBIDDEN,
                         INTERNAL_SERVER_ERROR, NOT_FOUND, OK, HTTPException)

from auth.decorator import login_required
from auth.function import GetUser
from flask import Blueprint, request
from marshmallow import Schema, ValidationError, fields, validate
from util.validate_request import ValidateRequest
from werkzeug.exceptions import HTTPException

from car.service import CarService

blueprint = Blueprint("car", __name__, url_prefix="/car")


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


@blueprint.route('/add', methods=['POST'])
@login_required
def add_car():
    user = GetUser()
    data = ValidateRequest(CarAddDto, request)
    CarService.add(user, data.car_license_plate, data.car_type)
    return {"message": "Car add."}, CREATED


@blueprint.route('/remove', methods=['DELETE'])
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


@blueprint.errorhandler(Exception)
def error_handle(err: Exception):
    if issubclass(type(err), ValidationError):
        return str(err), BAD_REQUEST
    if issubclass(type(err), HTTPException):
        return {'error': err.description}, err.code
    return {'message': "Internal server exception!"}, INTERNAL_SERVER_ERROR
