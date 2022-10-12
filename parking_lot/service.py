from typing import List

from database.database import db_session
from werkzeug.exceptions import InternalServerError

from parking_lot.model import ParkingLot


class CustomAvailableParkingLot:
    id: int
    location: str
    open_status: bool
    available: bool

    @classmethod
    def from_raw(cls, raw):
        obj = cls()
        obj.id = raw["id"]
        obj.location = raw["location"]
        obj.open_status = raw["open_status"]
        obj.available = raw["available"]
        return obj

    def json(self):
        return {
            "id": self.id,
            "location": self.location,
            "open_status": self.open_status,
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
        exec = db_session.execute(
            """
            SELECT
                DISTINCT t1.id,
                t1.location,
                t1.open_status,
                ANY_VALUE(t1.available) AS available
            FROM (
                SELECT 
                    parking_lots.id,
                    parking_lots.location,
                    parking_lots.open_status,
                    (
                        CASE
                            WHEN reservations.end_time IS NOT NULL AND parking_lots.open_status = 1 THEN 1
                            ELSE 0
                        END
                    ) AS available
                FROM
                    parking_lots
                LEFT JOIN
                    reservations
                ON 
                    parking_lots.id = reservations.parking_lot_id
                ORDER BY
                    parking_lots.id ASC
            )  AS t1
            GROUP BY
                t1.id
            ORDER BY 
                t1.id ASC
        """
        )

        result = exec.all()
        parsed = []

        for obj in result:
            new_obj = CustomAvailableParkingLot.from_raw(obj)
            parsed.append(new_obj)

        return parsed

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
