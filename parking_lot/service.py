from typing import List

from database.database import db_session
from werkzeug.exceptions import InternalServerError

from parking_lot.model import ParkingLot


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
            raise InternalServerError(
                "Something error when adding parking lot")

    @staticmethod
    def remove(parking_lot: ParkingLot):
        db_session.delete(parking_lot)
        db_session.commit()

    @staticmethod
    def find_by_id(id: int):
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
                            reservation.*,
                            (
                                CASE
                                    WHEN reservation.end_time IS NULL THEN "parking"
                                    ELSE "ended"
                                END
                            ) AS parking_status
                        FROM 
                            reservation
                    ) AS t1 
                WHERE
                    t1.parking_status = "parking"
                    AND
                    t1.parking_lot_id = :parking_lot_id
            """,
            {"parking_lot_id": parking_lot.id}
        )

        return len(result.all()) == 0

    @staticmethod
    def get_all_parking_lot_with_available_status():
        result = db_session.execute(
            """
            SELECT
                DISTINCT t1.id,
                t1.location,
                t1.open_status,
                ANY_VALUE(t1.available) AS available
            FROM (
                SELECT 
                    parking_lot.id,
                    parking_lot.location,
                    parking_lot.open_status,
                    (
                        CASE
                            WHEN reservation.end_time IS NOT NULL AND parking_lot.open_status = 1 THEN 1
                            ELSE 0
                        END
                    ) AS available
                FROM
                    parking_lot
                LEFT JOIN
                    reservation
                ON 
                    parking_lot.id = reservation.parking_lot_id
                ORDER BY
                    parking_lot.id ASC
            )  AS t1
            GROUP BY
                t1.id
            ORDER BY 
                t1.id ASC
        """
        )

        return result.all()
