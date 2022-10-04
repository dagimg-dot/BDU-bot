from telebot import TeleBot
from telebot.types import Message
from util.useful_lists import *
from util.keyboard_buttons import buttons
from util.validate_login import *
from handlers.back_button_handler import back_button_handler
from functionalities.SIMS.bdu_sims_login import login
from functionalities.GPA_Prediction.gpa_prediction_menu import predict_gpa



def main_messages(message: Message, bot: TeleBot):
    if message.text not in Buttons:
        bot.send_message(message.from_user.id,
                             "I didn't get what you say ...")
    elif message.text == menu[0]:
        # login(message)
        login(message)
        # bot.send_message(message.chat.id," To Login",reply_markup=buttons("s_login"))
    elif message.text == menu[1]:
        # markup = telebot.types.ReplyKeyboardRemove()
        # gpa_calculator.gpa_prediction(message)
        predict_gpa(message)
        # bot.send_message(message.chat.id,"Predict GPA")
        # msg = "This is a GPA Prediction Tool. To use it please enter your department . . ."
        # bot.send_message(message.from_user.id, msg, reply_markup=markup)
    elif master_check == True:
        if message.text == success_login[0]:
            buttons_clicked.append(message.text)
            bot.send_message(message.from_user.id, success_login[0],
                             reply_markup=buttons("my_courses"))
        elif message.text == success_login[1]:
            buttons_clicked.append(message.text)
            bot.send_message(message.from_user.id, success_login[1],
                             reply_markup=buttons("my_status"))
        elif message.text == success_login[2]:
            bot.send_message(message.from_user.id, "Pulling Grades ... ",
                             reply_markup=buttons("s_login"))
            # My_Grades(message)
            bot.send_message(message.chat.id,"My Grades")
        elif message.text == success_login[3]:
            bot.send_message(message.from_user.id, success_login[3],
                             reply_markup=buttons("s_login"))
        elif message.text == MyC[0]:
            bot.send_message(message.from_user.id, "Pulling all courses . . .",
                             reply_markup=buttons("my_courses"))
            bot.send_message(message.chat.id,"My Status")
        elif message.text == MyC[1]:
            msg = bot.send_message(message.from_user.id, "Enter year",
                                   reply_markup=buttons("my_courses"))
            choice = 'y'
            bot.register_next_step_handler(msg, course_year_handler, choice)
        elif message.text == MyC[2]:
            msg = bot.send_message(message.from_user.id, "Enter year",
                                   reply_markup=buttons("my_courses"))
            choice = 's'
            bot.register_next_step_handler(msg, course_year_handler, choice)
        elif message.text == MyS[0]:
            current_cgpa(message)
        elif message.text == MyS[1]:
            msg = bot.send_message(message.from_user.id, "Enter year",
                                   reply_markup=buttons("my_status"))
            bot.register_next_step_handler(msg, status_year_handler)
        elif message.text == MyS[2]:
            msg = bot.send_message(message.from_user.id, "Enter year",
                                   reply_markup=buttons("my_status"))
            bot.register_next_step_handler(msg, sgrade_year_handler)
        elif message.text == "Back":
            back_button_handler(message,bot)
        elif message.text == "Back to Menu":
            still_loggedin_checker(message)
    elif master_check == False:
        bot.send_message(
            message.chat.id, "You are not logged in yet , please press Login button and continue.")