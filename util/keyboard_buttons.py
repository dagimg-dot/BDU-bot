from telebot import types
from util.useful_lists import *


def buttons(type="Menu"):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,input_field_placeholder="BDU SIMS")
    if type == "Menu":
        row = [types.KeyboardButton(x) for x in menu[:2]]
        row_r = types.KeyboardButton(menu[2]) 
        markup.add(*row)
        markup.add(row_r)
    elif type == "s_login":
        row = [types.KeyboardButton(x) for x in success_login]
        markup.add(*row)
        markup.add(types.KeyboardButton("Back to Menu (Log Out)"))
    elif type == "my_courses":
        markup.row_width = 1
        row = [types.KeyboardButton(x) for x in MyC]
        markup.add(*row)
        markup.add(types.KeyboardButton("Back"),
                   types.KeyboardButton("Back to Menu (Log Out)"))
    elif type == "my_status":
        markup.row_width = 1
        row = [types.KeyboardButton(x) for x in MyS]
        markup.add(*row)
        markup.add(types.KeyboardButton("Back"),
                   types.KeyboardButton("Back to Menu (Log Out)"))
    return markup


