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
    CarService.add(user, "A-11111", "Tesla Car")
    CarService.add(user, "A-22222", "Starship Rocket")
    CarService.add(user, "A-33333", "Falcon Nine Rocket")
