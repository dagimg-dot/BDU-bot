from telebot import TeleBot
from telebot.types import Message
from util.state_holder import user_state_changer
from util.useful_lists import *
from functionalities.SIMS.bdu_sims_login import login
from functionalities.GPA_Prediction.gpa_prediction_menu import predict_gpa
from handlers.login_functionalities_menu import functionalities_menu_messages


def main_menu_messages(message: Message, bot: TeleBot):
    if message.text in Buttons:
        if message.text in menu:
            if message.text == menu[0]:
                login(message)
            elif message.text == menu[1]:
                user_state_changer(message,menu[1])
                predict_gpa(message)
            elif message.text == menu[2]:
                user_state_changer(message,menu[2])
                predict_gpa(message)
        else:
            functionalities_menu_messages(message)
    else:
        bot.send_message(message.from_user.id,"I didn't get what you say ...")
