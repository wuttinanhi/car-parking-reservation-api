"""
    auth blueprint
"""


from http.client import OK

from auth.decorator import admin_only
from flask import Blueprint, request
from marshmallow import Schema, fields, validate
from util.validate_request import validate_request

from settings.model import Setting
from settings.service import SettingService

blueprint = Blueprint("settings", __name__, url_prefix="/settings")


class SettingDto(Schema):
    charge_within_hour = fields.Float(required=True, validate=validate.Range(min=0))
    charge_more_than_a_hour = fields.Float(
        required=True, validate=validate.Range(min=0)
    )
    charge_more_than_a_day = fields.Float(required=True, validate=validate.Range(min=0))


@blueprint.route("/set", methods=["POST"])
@admin_only
def set_settings():
    data = validate_request(SettingDto, request)
    settings = Setting(
        data.charge_within_hour,
        data.charge_more_than_a_hour,
        data.charge_more_than_a_day,
    )
    SettingService.set_settings(settings)
    return {"message": "Setting complete."}, OK


@blueprint.route("/get", methods=["GET"])
def get_settings():
    setting = SettingService.get_settings()
    return setting.json()
