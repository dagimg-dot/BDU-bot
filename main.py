from handlers.commands_user import start_message,help_message,menu_handler
from handlers.main_menu import main_menu_messages
from util.user_fetch import fetchUsers
from bot import bot


print("Bot started ...")

# Handles all commands the bot supports
def command_handlers():
    bot.register_message_handler(start_message, commands=['start'], pass_bot=True)
    bot.register_message_handler(help_message, commands=['help'], pass_bot=True)
    bot.register_message_handler(menu_handler, commands=['menu'], pass_bot=True)
    
# Handles all incoming button clicks and messages
def message_handlers():
    bot.register_message_handler(main_menu_messages,pass_bot=True)

command_handlers()

message_handlers()

fetchUsers()

def run():
    bot.infinity_polling()

run()
