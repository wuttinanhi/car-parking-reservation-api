"""
    chat seed
"""


def seed_chat():
    print("Mocking chat...")

    from chat.service import ChatService
    from user.service import UserService

    # create user
    annie = UserService.find_by_email("annie@example.com")
    bobbie = UserService.find_by_email("bobbie@example.com")
    charlie = UserService.find_by_email("charlie@example.com")

    # mock dummy chat
    # annie -> bobbie
    ChatService.send_chat(annie, bobbie, "Hello Bobbie!")
    ChatService.send_chat(bobbie, annie, "Hi Annie!")
    ChatService.send_chat(annie, bobbie, "Can you move your car?")
    ChatService.send_chat(bobbie, annie, "Sure!")

    # bobbie -> charlie
    ChatService.send_chat(bobbie, charlie, "Hi Charlie!")
    ChatService.send_chat(charlie, bobbie, "Hello Bobbie!")

    # annie -> charlie
    ChatService.send_chat(annie, charlie, "Hello Charlie!")
    ChatService.send_chat(charlie, annie, "Hi Annie!")


if __name__ == "__main__":
    pass
