"""
    user seed
"""


def seed_user():
    from user.service import UserService

    print("Mocking user...")

    UserService.register(
        "root@example.com",
        "root-password",
        "root",
        "root-firstname",
        "root-lastname",
        "0000000000",
        "0000000000000",
    )

    UserService.register(
        "annie@example.com",
        "annie-password",
        "annie",
        "annie-firstname",
        "annie-lastname",
        "1111111111",
        "1111111111111",
    )

    UserService.register(
        "bobbie@example.com",
        "bobbie-password",
        "bobbie",
        "bobbie-firstname",
        "bobbie-lastname",
        "2222222222",
        "2222222222222",
    )

    UserService.register(
        "charlie@example.com",
        "charlie-password",
        "charlie",
        "charlie-firstname",
        "charlie-lastname",
        "3333333333",
        "3333333333333",
    )

