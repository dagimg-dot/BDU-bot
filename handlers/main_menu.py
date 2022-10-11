from telebot import TeleBot
from telebot.types import Message
from util.useful_lists import *
from util.keyboard_buttons import buttons
from functionalities.SIMS.bdu_sims_login import login
from functionalities.GPA_Prediction.gpa_prediction_menu import predict_gpa
from handlers.functionalities_menu import functionalities_menu_messages


def main_menu_messages(message: Message, bot: TeleBot):
    if message.text in Buttons:
        if message.text in menu:
            if message.text == menu[0]:
                bot.send_message(message.from_user.id, "Func Menu", reply_markup=buttons("s_login"))
                login(message)
            elif message.text == menu[1]:
                predict_gpa(message)
        else:
            functionalities_menu_messages(message)
    else:
        bot.send_message(message.from_user.id,"I didn't get what you say ...")
