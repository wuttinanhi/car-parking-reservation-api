"""

    chat example
    
    run: 
        python -m example.chat

"""
from database.database import init_db
from env_wrapper import load_env
from pagination.pagination import PaginationSortOptions
from user.service import UserService

from chat.service import ChatHistoryPaginationOptions, ChatService

# setup
load_env()
init_db()

# list chat history
from_user = UserService.find_by_id(2)
to_user = UserService.find_by_id(3)

opts = ChatHistoryPaginationOptions()
opts.page = 1
opts.limit = 20
opts.sort = PaginationSortOptions.DESC
opts.order_by = "send_date"
opts.search = ""

opts.from_user_id = from_user.id
opts.to_user_id = to_user.id


chats = ChatService.list_chat_history(opts)

for chat in chats:
    print(chat)

print("=" * 10)

# get last chat message
from_user = UserService.find_by_id(2)
to_user = UserService.find_by_id(3)

last_chat_message = ChatService.get_last_chat_message(from_user, to_user)
print(last_chat_message)
