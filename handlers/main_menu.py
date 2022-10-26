from telebot import TeleBot
from telebot.types import Message
from util.keyboard_buttons import buttons
from util.state_holder import user_state_changer
from util.useful_lists import *
from functionalities.SIMS.bdu_sims_login import login
from functionalities.GPA_Prediction.gpa_prediction_menu import predict_gpa
from handlers.login_functionalities_menu import functionalities_menu_messages
from util.user_database import users


def main_menu_messages(message: Message, bot: TeleBot):
    if message.text in Buttons:
        if message.text in menu:
            if message.text == menu[0]:
                # bot.send_message(message.chat.id,"yme",reply_markup=buttons("s_login"))
                login(message)
            elif message.text == menu[1]:
                user_state_changer(message,menu[1])
                predict_gpa(message)
            elif message.text == menu[2]:
                user_state_changer(message,menu[2])
                # print(users[message.from_user.id].gpa_list)
                predict_gpa(message)
        else:
            functionalities_menu_messages(message)
    else:
        bot.send_message(message.from_user.id,"I didn't get what you say ...")
