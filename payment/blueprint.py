"""
    payment blueprint
"""

import json
from http.client import FORBIDDEN, NOT_FOUND

import stripe
from auth.decorator import login_required
from auth.function import GetUser
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields
from pagination.pagination import create_pagination_options_from_request
from util.validate_request import ValidateRequest

from payment.service import PaymentService

blueprint = Blueprint("payment", __name__, url_prefix="/payment")


class PayInvoiceDto(Schema):
    invoice_id = fields.Int(required=True)


@blueprint.route("/my_invoice", methods=["GET"])
@login_required
def list_user_invoice():
    user = GetUser()
    response_list = []
    pagination_options = create_pagination_options_from_request(request)
    result = PaymentService.paginate_user_invoice(user, pagination_options)
    for invoice in result:
        response_list.append(invoice.json())
    return response_list


@blueprint.route("/pay", methods=["POST"])
@login_required
def pay_invoice():
    user = GetUser()
    data = ValidateRequest(PayInvoiceDto, request)
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
        print("⚠️  Webhook error while parsing basic request." + str(e))
        return jsonify(success=False)

    # get signature header
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, PaymentService.stripe_webhook_secret
        )
    except stripe.error.SignatureVerificationError as e:
        print("⚠️  Webhook signature verification failed." + str(e))
        return jsonify(success=False)

    # check event is none
    if event == None:
        raise jsonify(success=False)

    # handle event
    if event and event["type"] == "payment_intent.succeeded":
        payment_intent: stripe.PaymentIntent = event["data"]["object"]
        PaymentService.handle_stripe_payment(payment_intent)
        print("Payment for {} succeeded".format(payment_intent["amount"]))
    else:
        # Unexpected event type
        print("Unhandled event type {}".format(event["type"]))

    # return success
    return jsonify(success=True)


@blueprint.route("/stripe/public_key", methods=["GET"])
def stripe_public_key():
    return PaymentService.stripe_public_key
