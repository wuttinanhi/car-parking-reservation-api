"""
    mock script
"""

# load env
from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    from car.service import CarService
    from database.database import Base, db_session, engine, init_db
    from user.service import UserService

    # drop all
    Base.metadata.drop_all(bind=engine)

    # setup database
    init_db()

    # mock user
    UserService.register("test@example.com", "@Test12345")

    # get user
    user = UserService.find_by_email("test@example.com")

    # mock user car
    CarService.add(user, "A11111", "Tesla")
    CarService.add(user, "A22222", "Starship")

    # get all car
    user_cars = CarService.find_all_car_by_user(user)
    for car in user_cars:
        print(car)

    # remove database session
    db_session.remove()
