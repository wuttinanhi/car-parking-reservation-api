from typing import List

from database.database import db_session
from werkzeug.exceptions import InternalServerError

from parking_lot.model import ParkingLot


class CustomAvailableParkingLot:
    parking_lot: ParkingLot
    available: bool

    def __init__(self, parking_lot: ParkingLot) -> None:
        self.parking_lot = parking_lot
        self.available = (
            ParkingLotService.is_parking_lot_available(self.parking_lot)
            and self.parking_lot.open_status
        )

    def json(self):
        return {
            "id": self.parking_lot.id,
            "location": self.parking_lot.location,
            "open_status": self.parking_lot.open_status,
            "available": self.available,
        }


class ParkingLotService:
    @staticmethod
    def add(location: str, open_status=False):
        try:
            parking_lot = ParkingLot(location, open_status)
            db_session.add(parking_lot)
            db_session.commit()
            return parking_lot
        except Exception as err:
            db_session.rollback()
            print(err)
            raise InternalServerError("Something error when adding parking lot")

    @staticmethod
    def update(parking_lot: ParkingLot):
        try:
            ParkingLot.query.filter(ParkingLot.id == parking_lot.id).update(
                {
                    "location": parking_lot.location,
                    "open_status": parking_lot.open_status,
                }
            )
            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()
            raise InternalServerError("Failed to update parking lot!")

    @staticmethod
    def remove(parking_lot: ParkingLot):
        db_session.delete(parking_lot)
        db_session.commit()

    @staticmethod
    def find_by_id(id: int) -> ParkingLot:
        return ParkingLot.query.filter(ParkingLot.id == id).first()

    @staticmethod
    def get_all_parking_lot() -> List[ParkingLot]:
        return ParkingLot.query.all()

    @staticmethod
    def get_open_parking_lot() -> List[ParkingLot]:
        return ParkingLot.query.filter(ParkingLot.open_status == True).all()

    @staticmethod
    def is_parking_lot_available(parking_lot: ParkingLot):
        result = db_session.execute(
            """
                SELECT 
                    *
                FROM 
                    (
                        SELECT
                            reservations.*,
                            (
                                CASE
                                    WHEN reservations.end_time IS NULL THEN "parking"
                                    ELSE "ended"
                                END
                            ) AS parking_status
                        FROM 
                            reservations
                    ) AS t1 
                WHERE
                    t1.parking_status = "parking"
                    AND
                    t1.parking_lot_id = :parking_lot_id
            """,
            {"parking_lot_id": parking_lot.id},
        )

        return len(result.all()) == 0

    @staticmethod
    def get_all_parking_lot_with_available_status() -> List[CustomAvailableParkingLot]:
        all_parking_lot = ParkingLotService.get_all_parking_lot()
        parsed = []
        for parking_lot in all_parking_lot:
            new_obj = CustomAvailableParkingLot(parking_lot)
            parsed.append(new_obj)
        return parsed
