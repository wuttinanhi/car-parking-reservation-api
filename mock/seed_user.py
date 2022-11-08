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
        "Root",
        "Admin",
        "0000000000",
        "0000000000000",
    )

    UserService.register(
        "annie@example.com",
        "annie-password",
        "annie",
        "Annie",
        "Carparker",
        "0101234567",
        "1111111111111",
    )

    UserService.register(
        "bobbie@example.com",
        "bobbie-password",
        "bobbie",
        "Bobbie",
        "Carparker",
        "0201234567",
        "2222222222222",
    )

    UserService.register(
        "charlie@example.com",
        "charlie-password",
        "charlie",
        "Charlie",
        "Carparker",
        "0301234567",
        "3333333333333",
    )
