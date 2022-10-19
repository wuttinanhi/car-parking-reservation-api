"""
    auth blueprint
"""


from http.client import CREATED, FORBIDDEN, NOT_FOUND, OK

from auth.decorator import admin_only, login_required
from auth.function import GetUser
from flask import Blueprint, request
from marshmallow import Schema, fields, validate
from pagination.pagination import create_pagination_options_from_request
from user.service import UserService
from util.validate_request import ValidateRequest
from werkzeug.exceptions import Forbidden

from car.service import CarService

blueprint = Blueprint("car", __name__, url_prefix="/car")


class CarAddDto(Schema):
    car_license_plate = fields.Str(
        required=True, validate=validate.Length(min=2, max=10)
    )
    car_type = fields.Str(required=True, validate=validate.Length(min=3, max=10))


class CarUpdateDto(CarAddDto):
    car_id = fields.Int(required=True)


class CarDeleteDto(Schema):
    car_id = fields.Int(required=True)


class CarSearchDto(Schema):
    car_license_plate = fields.Str(
        required=True, validate=validate.Length(min=2, max=10)
    )


@blueprint.route("/add", methods=["POST"])
@login_required
def add_car():
    user = GetUser()
    data = ValidateRequest(CarAddDto, request)
    CarService.add(user, data.car_license_plate, data.car_type)
    return {"message": "Car add."}, CREATED


@blueprint.route("/remove", methods=["DELETE"])
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
    return {"error": "Car not found!"}, NOT_FOUND


@blueprint.route("/my_car", methods=["GET"])
@login_required
def my_car():
    response = []
    user = GetUser()
    all_user_cars = CarService.find_all_car_by_user(user)
    for car in all_user_cars:
        response.append(car.json())
    return response


@blueprint.route("/update", methods=["PATCH"])
@login_required
def update_car():
    user = GetUser()
    data = ValidateRequest(CarUpdateDto, request)
    car = CarService.find_by_id(data.car_id)

    if car.car_owner_id != user.id:
        raise Forbidden("Car not owned by user!")

    car.car_license_plate = data.car_license_plate
    car.car_type = data.car_type

    CarService.update(car)
    return {"message": "Successfully updated car."}, 200


@blueprint.route("/search", methods=["GET"])
@login_required
def search_car_by_license_plate():
    data = ValidateRequest(CarSearchDto, request)
    car = CarService.find_by_license_plate(data.car_license_plate)
    response = car.json()
    response["car_owner"] = UserService.find_by_id(car.car_owner_id).json_shareable()
    return response


@blueprint.route("/admin/list", methods=["GET"])
@admin_only
def admin_pagination_car():
    pagination_options = create_pagination_options_from_request(request)
    result = CarService.admin_pagination_car(pagination_options)
    response = []
    for obj in result:
        response.append(obj.json())
    return response
