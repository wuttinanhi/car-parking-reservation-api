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
    ChatService.send_chat(annie, bobbie, "1 start Hello Bobbie!")
    ChatService.send_chat(bobbie, annie, "2 Hi Annie!")
    ChatService.send_chat(annie, bobbie, "3 How are you?")
    ChatService.send_chat(bobbie, annie, "4 end I'm good!")

    ChatService.send_chat(bobbie, charlie, "1 start Hello Charlie!")
    ChatService.send_chat(charlie, bobbie, "2 end Hi Bobbie!")

    ChatService.send_chat(annie, charlie, "1 start Hello Charlie!")
    ChatService.send_chat(charlie, annie, "2 end Hi Annie!")


if __name__ == "__main__":
    pass
