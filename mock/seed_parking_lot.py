"""
    seed parking lot
"""


def seed_parking_lot():
    from parking_lot.service import ParkingLotService

    print("Mocking parking lot...")

    ParkingLotService.add("Floor 1", True)
    ParkingLotService.add("Floor 2", True)
    ParkingLotService.add("Floor 3", False)
