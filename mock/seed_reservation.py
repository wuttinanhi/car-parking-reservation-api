"""
    seed reservation
"""


def seed_reservation():
    print("Mocking reservation...")

    from datetime import datetime, timedelta

    from car.service import CarService
    from parking_lot.service import ParkingLotService
    from payment.service import PaymentService
    from reservation.service import ReservationService
    from user.service import UserService

    user = UserService.find_by_id(2)
    car_1 = CarService.find_by_id(1)
    parking_lot_1 = ParkingLotService.find_by_id(1)

    for i in range(1, 11):
        parking_date = datetime(year=2022, month=1, day=1, hour=i, minute=0, second=0)

        # mock reservation
        reservation = ReservationService.create_reservation(
            user, car_1, parking_lot_1, parking_date
        )

        if i < 10:
            # end created reservation
            ReservationService.end_reservation(
                reservation, reservation.start_time + timedelta(hours=1)
            )

            # create invoice
            invoice = PaymentService.create_invoice(reservation)
            invoice.charge_amount = PaymentService.calculate_charge(reservation)
            PaymentService.update_invoice(invoice)
