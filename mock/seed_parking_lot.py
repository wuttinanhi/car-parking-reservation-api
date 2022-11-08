"""
    seed parking lot
"""


def seed_parking_lot():
    from parking_lot.service import ParkingLotService

    print("Mocking parking lot...")

    for building in range(1, 5):
        for floor in range(1, 5):
            for lot in range(1, 10):
                ParkingLotService.add(
                    f"Building {building} Floor {floor} Lot {lot}", True
                )
