"""
    seed car
"""


def seed_car():
    from car.service import CarService
    from user.service import UserService

    print("Mocking car...")

    # get root user
    user = UserService.find_by_email("annie@example.com")

    # mock user car
    CarService.add(user, "A11111", "Tesla")
    CarService.add(user, "A22222", "Starship")
    CarService.add(user, "A33333", "Falcon9")
