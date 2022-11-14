import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String

from database import Base


class InvoiceStatus(enum.Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    CANCELED = "CANCELED"
    REFUNDED = "REFUNDED"

    def __str__(self):
        return str(self.value)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    reservation_id = Column(Integer(), ForeignKey("reservations.id"), nullable=False)

    create_date = Column(DateTime(), nullable=False)
    stripe_payment_id = Column(String(100))

    charge_amount = Column(Float(), nullable=False)
    status = Column(Enum(InvoiceStatus), nullable=False)
    description = Column(String(255))

    def __init__(
        self,
        user_id: int,
        reservation_id: int,
        charge_amount: float,
        create_date: datetime,
        status: enum,
        description: str,
    ):
        self.user_id = user_id
        self.reservation_id = reservation_id
        self.charge_amount = charge_amount
        self.create_date = create_date
        self.status = status
        self.description = description

    def __repr__(self):
        return f"<Invoice {self.id}>"

    def json(self):
        return {
            "invoice_id": self.id,
            "invoice_user_id": self.user_id,
            "invoice_reservation_id": self.reservation_id,
            "invoice_charge_amount": self.charge_amount,
            "invoice_create_date": self.create_date,
            "invoice_status": str(self.status),
            "invoice_description": self.description,
        }
