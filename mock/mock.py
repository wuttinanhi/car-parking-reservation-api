"""
    mock class
"""


from chat.service import ChatService as _
from database.database import db_session, engine, init_db
from settings.service import SettingService

from mock.seed_car import seed_car
from mock.seed_chat import seed_chat
from mock.seed_parking_lot import seed_parking_lot
from mock.seed_reservation import seed_reservation
from mock.seed_user import seed_user


class Mock:
    # drop all
    @staticmethod
    def clean_db():
        try:
            with engine.connect() as conn:
                conn.execute("SET FOREIGN_KEY_CHECKS=0")
                conn.execute(
                    "DROP TABLE `cars`, `chats`, `chat_heads`, `invoices`, `parking_lots`, `reservations`, `settings`, `users`"
                )
                conn.execute("SET FOREIGN_KEY_CHECKS=1")
        except Exception as e:
            print(e)

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

        # mock car
        seed_car()

        # mock parking lot
        seed_parking_lot()

        # mock reservation
        seed_reservation()

        # remove database session
        db_session.remove()

        print("Mocking complete!")
