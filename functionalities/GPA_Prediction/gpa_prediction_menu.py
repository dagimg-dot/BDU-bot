from bot import bot
from telebot import types
import json
from functionalities.GPA_Prediction.additional_info import get_add_info
from util.useful_lists import dept_title


def predict_gpa(message):
    markup = types.InlineKeyboardMarkup() 
    markup.row_width = 1
    dept_buttons = [types.InlineKeyboardButton(x,callback_data=x) for x in dept_title]
    markup.add(*dept_buttons)
    bot.send_message(
        message.chat.id, 'Choose Department',reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def user_answer_dept(call):
    message = call.message
    if call.data == dept_title[0]:
        msg = dept_title[0]
        bot.answer_callback_query(call.id,"You Chose "+msg)
        get_add_info(message,msg)
    elif call.data == dept_title[1]:
        msg = dept_title[1]
        bot.answer_callback_query(call.id,"You Chose "+msg)
        get_add_info(message,msg)
    elif call.data == dept_title[2]:
        msg = dept_title[2]
        bot.answer_callback_query(call.id,"You Chose "+msg)
        get_add_info(message,msg)
    elif call.data == dept_title[3]:
        msg = dept_title[3]
        bot.answer_callback_query(call.id,"You Chose "+msg)
        get_add_info(message,msg)
    elif call.data == dept_title[4]:
        msg = dept_title[4]
        bot.answer_callback_query(call.id,"You Chose "+msg)
        get_add_info(message,msg)

