from telebot import TeleBot
from telebot.types import Message
from util.keyboard_buttons import buttons
from util.validate_login import buttons_clicked

def back_button_handler(message: Message, bot: TeleBot):
    length = len(buttons_clicked)
    if length != 1:
        for i in buttons_clicked[:length-1]:
            buttons_clicked.remove(i)
    if buttons_clicked[0] == "My Courses" or buttons_clicked[0] == "My Status":
        bot.send_message(message.from_user.id, "Back",
                         reply_markup=buttons())
        # bot.delete_message(message.chat.id,message.message_id)
        