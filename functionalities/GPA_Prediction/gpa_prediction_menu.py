from bot import bot
from telebot import types
from functionalities.GPA_Prediction.additional_info import get_add_info
from util.useful_lists import dept_title


def predict_gpa(message):
    markup = types.InlineKeyboardMarkup() 
    markup.row_width = 1
    dept_buttons = [types.InlineKeyboardButton(x,callback_data=x) for x in dept_title]
    markup.add(*dept_buttons)
    bot.send_message(message.chat.id, 'Choose Department',reply_markup=markup)

@bot.callback_query_handler(lambda query: query.data in dept_title)
def user_answer_dept(query):
    message = query.message
    for i in range(len(dept_title)):
        if query.data == dept_title[i]:
            msg = dept_title[i]
            bot.answer_callback_query(query.id,"You Chose "+msg)
            get_add_info(message,msg)

