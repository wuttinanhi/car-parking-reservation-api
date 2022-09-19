"""
    mock script
"""

# load env
from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    from services.car.car import CarService
    from services.database import Base, db_session, engine, init_db
    from services.user.user import UserService

    # drop all
    Base.metadata.drop_all(bind=engine)

    # setup database
    init_db()

    # mock user
    try:
        UserService.register("test@example.com", "@Test12345")
    except Exception:
        pass

    # get user
    user = UserService.find_by_email("test@example.com")

    # mock user car
    try:
        CarService.add(user, "A11111", "Tesla")
    except Exception:
        pass

    try:
        CarService.add(user, "A22222", "Starship")
    except Exception:
        pass

    # get all car
    user_cars = CarService.find_all_car_by_user(user)
    for car in user_cars:
        print(car)

    # remove database session
    db_session.remove()
