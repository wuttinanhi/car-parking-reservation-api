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
    ChatService.send_chat(annie, bobbie, "Hello Bobbie!")
    ChatService.send_chat(bobbie, annie, "Hi Annie!")
    ChatService.send_chat(annie, bobbie, "How are you?")
    ChatService.send_chat(bobbie, annie, "I'm good!")

    ChatService.send_chat(bobbie, charlie, "Hello Charlie!")
    ChatService.send_chat(charlie, bobbie, "Hi Bobbie!")


if __name__ == "__main__":
    pass
