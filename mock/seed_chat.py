"""
    mock chat script
"""

def seed_chat():
    from chat.service import ChatService
    from user.service import UserService

    print("Start mock chat...")

    # create user
    annie = UserService.register("annie@example.com", "annie-password")
    bobbie = UserService.register("bobbie@example.com", "bobbie-password")
    charlie = UserService.register("charlie@example.com", "charlie-password")

    # mock dummy chat
    ChatService.send_chat(annie, bobbie, "Hello Bobbie!")
    ChatService.send_chat(bobbie, annie, "Hi Annie!")
    ChatService.send_chat(annie, bobbie, "How are you?")
    ChatService.send_chat(bobbie, annie, "I'm good!")
    
    ChatService.send_chat(annie, charlie, "Hello Charlie!")

if __name__ == "__main__":
    pass
