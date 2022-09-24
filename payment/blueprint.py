'''
    payment blueprint
'''


from auth.decorator import login_required
from auth.function import GetUser
from flask import Blueprint
from marshmallow import Schema, fields, validate

from payment.service import PaymentService

blueprint = Blueprint("payment", __name__, url_prefix="/payment")


class Payment(Schema):
    location = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    open_status = fields.Boolean(required=True)


class ParkingLotDeleteDto(Schema):
    parking_lot_id = fields.Int(required=True)


@blueprint.route('/user_invoice', methods=['GET'])
@login_required
def list_user_invoice():
    user = GetUser()
    response = []
    list = PaymentService.get_all_user_invoice(user)
    for invoice in list:
        response.append(invoice.json())
    return response


@blueprint.route('/pay', methods=['POST'])
@login_required
def pay_invoice():
    # TODO: need implement
    user = GetUser()
    return None
