"""
    payment blueprint
"""

import json
from http.client import FORBIDDEN, NOT_FOUND, OK

import stripe
from flask import Blueprint, current_app, jsonify, request
from marshmallow import Schema, fields, validate

from auth.decorator import admin_only, login_required
from auth.function import get_user
from pagination.pagination import create_pagination_options_from_request
from payment.model import InvoiceStatus
from payment.service import PaymentService
from util.validate_request import validate_request

blueprint = Blueprint("payment", __name__, url_prefix="/payment")


class PayInvoiceDto(Schema):
    invoice_id = fields.Int(required=True)


class InvoiceUpdateDto(Schema):
    invoice_id = fields.Int(required=True)
    charge_amount = fields.Float(required=True, validate=validate.Range(min=0))
    status = fields.Enum(InvoiceStatus, required=True)
    description = fields.String(required=True, validate=validate.Length(max=255))


@blueprint.route("/list", methods=["GET"])
@login_required
def list_user_invoice():
    user = get_user()
    response_list = []
    pagination_options = create_pagination_options_from_request(request)
    result = PaymentService.paginate_user_invoice(user, pagination_options)
    for invoice in result:
        response_list.append(invoice.json())
    return response_list


@blueprint.route("/pay", methods=["POST"])
@login_required
def pay_invoice():
    user = get_user()
    data = validate_request(PayInvoiceDto, request)
    invoice = PaymentService.get_invoice_by_id(data.invoice_id)

    if invoice == None:
        return {"error": "Invoice not found!"}, NOT_FOUND

    if invoice.user_id != user.id:
        return {"error": "Invoice not own by user!"}, FORBIDDEN

    if invoice:
        intent = PaymentService.create_pay_token(invoice)
        return {"stripe_client_secret": intent.client_secret}


@blueprint.route("/stripe/webhook", methods=["POST"])
def stripe_webhook():
    event = None
    payload = request.data

    # try load json payload
    try:
        event = json.loads(payload)
    except:
        current_app.logger.error(
            "??????  Webhook error while parsing basic request." + str(e)
        )
        return jsonify(success=False)

    # get signature header
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, PaymentService.stripe_webhook_secret
        )
    except stripe.error.SignatureVerificationError as e:
        current_app.logger.error("??????  Webhook signature verification failed." + str(e))
        return jsonify(success=False)

    # check event is none
    if event == None:
        raise jsonify(success=False)

    # handle event
    if event and event["type"] == "payment_intent.succeeded":
        payment_intent: stripe.PaymentIntent = event["data"]["object"]
        PaymentService.handle_stripe_payment(payment_intent)
        current_app.logger.info(
            "Payment for {} succeeded".format(payment_intent["amount"])
        )
    else:
        # Unexpected event type
        current_app.logger.error("Unhandled event type {}".format(event["type"]))

    # return success
    return jsonify(success=True)


@blueprint.route("/stripe/public_key", methods=["GET"])
def stripe_public_key():
    return PaymentService.stripe_public_key


@blueprint.route("/admin/list", methods=["GET"])
@admin_only
def admin_invoice_list():
    response_list = []
    pagination_options = create_pagination_options_from_request(request)
    result = PaymentService.admin_list_payment(pagination_options)
    for obj in result:
        response_list.append(obj.json())
    return response_list


@blueprint.route("/admin/update", methods=["PATCH"])
@admin_only
def admin_invoice_update():
    data = validate_request(InvoiceUpdateDto, request)
    invoice = PaymentService.get_invoice_by_id(data.invoice_id)

    invoice.charge_amount = data.charge_amount
    invoice.status = data.status
    invoice.description = data.description

    PaymentService.update_invoice(invoice)
    return {"message": "Successfully updated invoice."}, OK
