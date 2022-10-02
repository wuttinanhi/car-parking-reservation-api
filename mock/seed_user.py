"""
    user seed
"""


def seed_user():
    from user.service import UserService

    root = UserService.register(
        "root@example.com",
        "root-password",
        "root",
        "root-firstname",
        "root-lastname",
        "0000000000",
    )
    annie = UserService.register(
        "annie@example.com",
        "annie-password",
        "annie",
        "annie-firstname",
        "annie-lastname",
        "1111111111",
    )
    bobbie = UserService.register(
        "bobbie@example.com",
        "bobbie-password",
        "bobbie",
        "bobbie-firstname",
        "bobbie-lastname",
        "2222222222",
    )
    charlie = UserService.register(
        "charlie@example.com",
        "charlie-password",
        "charlie",
        "charlie-firstname",
        "charlie-lastname",
        "3333333333",
    )
