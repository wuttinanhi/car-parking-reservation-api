'''
    payment blueprint
'''


from http.client import FORBIDDEN, NOT_FOUND

from auth.decorator import login_required
from auth.function import GetUser
from flask import Blueprint, request
from marshmallow import Schema, fields
from util.validate_request import ValidateRequest

from payment.service import PaymentService

blueprint = Blueprint("payment", __name__, url_prefix="/payment")


class PayInvoiceDto(Schema):
    invoice_id = fields.Int(required=True)


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
    user = GetUser()
    data = ValidateRequest(PayInvoiceDto, request)
    invoice = PaymentService.get_invoice_by_id(data.invoice_id)

    if invoice == None:
        return {"error": "Invoice not found!"}, NOT_FOUND
    if invoice.user_id == user.id:
        return {"error": "Invoice not own by user!"}, FORBIDDEN
    if invoice:
        stripe_client_secret = PaymentService.create_pay_token(invoice)
        return {"stripe_client_secret": stripe_client_secret}
