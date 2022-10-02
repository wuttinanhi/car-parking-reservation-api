"""
    mock class
"""

from datetime import datetime, timedelta

from car.service import CarService
from database.database import Base, db_session, engine, init_db
from parking_lot.service import ParkingLotService
from payment.service import PaymentService
from reservation.service import ReservationService
from settings.service import SettingService
from user.service import UserService

from mock.seed_chat import seed_chat
from mock.seed_user import seed_user


class Mock:
    # drop all
    @staticmethod
    def clean_db():
        init_db()
        Base.metadata.drop_all(bind=engine)

    # setup database
    @staticmethod
    def setup_db():
        init_db()

    @staticmethod
    def mock():
        # mock setting
        SettingService.setup_default_settings()

        # mock user
        seed_user()

        # mock chat
        seed_chat()

        # get root user
        user = UserService.find_by_email("root@example.com")

        # mock user car
        car_1 = CarService.add(user, "A11111", "Tesla")
        car_2 = CarService.add(user, "A22222", "Starship")
        car_3 = CarService.add(user, "A33333", "Falcon9")

        # get all car
        # user_cars = CarService.find_all_car_by_user(user)
        # for car in user_cars:
        #     print(car)

        # mock parking lot
        parking_lot_1 = ParkingLotService.add("Floor 1", True)
        parking_lot_2 = ParkingLotService.add("Floor 2", True)
        parking_lot_3 = ParkingLotService.add("Floor 3", False)

        for i in range(1, 50):
            # mock reservation
            reservation = ReservationService.create_reservation(
                user, car_1, parking_lot_1, datetime.utcnow()
            )

            # end created reservation
            ReservationService.end_reservation(
                reservation, reservation.start_time + timedelta(hours=1)
            )

            # create invoice
            invoice = PaymentService.create_invoice(reservation)
            invoice.charge_amount = i * 10
            PaymentService.update_invoice(invoice)

        seed_chat()

        # try:
        #     PaymentService.setup_payment()
        #     invoice = PaymentService.create_invoice(reservation)

        #     intent = PaymentService.create_pay_token(invoice)

        #     print(intent.client_secret)
        #     print(intent.id)

        #     PaymentService.handle_stripe_payment(intent)
        # except Exception as err:
        #     print(err)

        # reservation_2 = ReservationService.create_reservation(
        #     user,
        #     car_1,
        #     parking_lot_1,
        #     datetime.utcnow()
        # )

        # reservation_2 = ReservationService.create_reservation(
        #     user,
        #     car_2,
        #     parking_lot_2,
        #     datetime.utcnow()
        # )

        # reservation_3 = ReservationService.create_reservation(
        #     user,
        #     car_3,
        #     parking_lot_3,
        #     datetime.utcnow()
        # )

        # debug
        # print(ParkingLotService.is_parking_lot_available(parking_lot_1))
        # print(ParkingLotService.is_parking_lot_available(parking_lot_2))
        # print(ParkingLotService.is_parking_lot_available(parking_lot_3))

        # try create reservation on busy parking lot
        # try:
        #     ReservationService.create_reservation(
        #         user,
        #         car_1,
        #         parking_lot_1,
        #         datetime.utcnow()
        #     )
        # except Exception as e:
        #     print(e)

        # try:
        #     ReservationService.end_reservation(reservation_2)
        #     t2_reserve = ReservationService.create_reservation(
        #         user,
        #         car_2,
        #         parking_lot_2,
        #         datetime.utcnow()
        #     )
        #     ReservationService.end_reservation(t2_reserve)
        # except Exception as e:
        #     print(e)

        # try:
        #     t_reserve = ReservationService.create_reservation(
        #         user,
        #         car_3,
        #         parking_lot_3,
        #         datetime.utcnow()
        #     )
        #     ReservationService.end_reservation(t_reserve)
        # except Exception as e:
        #     print(e)

        # remove database session
        db_session.remove()
