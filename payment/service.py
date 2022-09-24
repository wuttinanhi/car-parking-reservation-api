"""
    payment service
"""
import os
from datetime import datetime
from typing import List

import stripe
from database.database import db_session
from reservation.model import Reservation
from settings.service import SettingService
from user.model import User
from werkzeug.exceptions import BadRequest, InternalServerError

from payment.model import Invoice, InvoiceStatus


class PaymentService:
    @staticmethod
    def setup_payment():
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    @staticmethod
    def calculate_charge(reservation: Reservation):
        setting = SettingService.get_settings()

        start_time: datetime = reservation.start_time
        end_time: datetime = reservation.end_time

        diff = end_time - start_time
        hour = divmod(diff.total_seconds(), 3600)[0]

        charge = 0

        if hour < 0:
            charge = setting.charge_within_hour
        if hour >= 1:
            charge = setting.charge_more_than_a_hour * hour
        if hour >= 24:
            day = round(hour / 24)
            charge = setting.charge_more_than_a_day * day

        return charge

    @staticmethod
    def create_invoice(reservation: Reservation, description=""):
        try:
            charge_amount = PaymentService.calculate_charge(reservation)

            invoice = Invoice(
                reservation.user_id,
                reservation.id,
                charge_amount,
                datetime.utcnow(),
                InvoiceStatus.UNPAID,
                description
            )

            # if charge amount is 0 set to paid
            if charge_amount <= 0:
                invoice.status = InvoiceStatus.PAID

            db_session.add(invoice)
            db_session.commit()

            return invoice
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to create invoice!")

    @staticmethod
    def update_invoice(invoice: Invoice):
        try:
            db_session.query(Invoice).update({
                "charge_amount": invoice.charge_amount,
                "status": invoice.status,
                "description": invoice.description
            })
            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to update invoice!")

    @staticmethod
    def get_invoice_by_id(id: int) -> Invoice:
        return Invoice.query.filter(Invoice.id == id).first()

    @staticmethod
    def get_invoice_by_reservation(reservation: Reservation) -> Invoice:
        return Invoice.query.filter(Invoice.reservation_id == reservation.id).first()

    @staticmethod
    def paginate_invoice():
        # TODO: need implement
        pass

    @staticmethod
    def get_all_user_invoice(user: User) -> List[Invoice]:
        return Invoice.query.filter(Invoice.user_id == user.id).all()

    @staticmethod
    def create_pay_token(invoice: Invoice):
        charge_amount = invoice.charge_amount

        if invoice.status != InvoiceStatus.UNPAID:
            raise BadRequest("Invoice status invalid!")

        if charge_amount < 10:
            raise BadRequest("Minimum charge is 10!")

        intent = stripe.PaymentIntent.create(
            amount=round(charge_amount * 100),
            currency="thb",
            payment_method_types=["card"]
        )

        invoice.stripe_payment_id = intent.id
        PaymentService.update_invoice(invoice)

        return intent.client_secret
