from telebot import TeleBot
from handlers.commands_user import start_message,help_message,menu_handler
from handlers.messages_user import main_messages
from bot import bot


print("Bot started ...")

# Handles all commands the bot supports
def command_handlers():
    bot.register_message_handler(start_message, commands=['start'], pass_bot=True)
    bot.register_message_handler(help_message, commands=['help'], pass_bot=True)
    bot.register_message_handler(menu_handler, commands=['menu'], pass_bot=True)
    
# Handles all incoming button clicks
def message_handlers():
    bot.register_message_handler(main_messages,pass_bot=True)


command_handlers()

message_handlers()


def run():
    bot.infinity_polling()


run()
