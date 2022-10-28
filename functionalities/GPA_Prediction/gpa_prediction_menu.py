from bot import bot
from telebot import types
from functionalities.GPA_Prediction.additional_info import get_add_info
from util.message_cleaner import cleaner
from util.useful_lists import dept_title
from util.user_database import users


def predict_gpa(message):
    markup = types.InlineKeyboardMarkup() 
    markup.row_width = 1
    dept_buttons = [types.InlineKeyboardButton(x,callback_data=x) for x in dept_title]
    markup.add(*dept_buttons)
    sent_msg = bot.send_message(message.chat.id, 'Choose Department',reply_markup=markup)
    users[message.from_user.id].message_id[3] = sent_msg.message_id

@bot.callback_query_handler(lambda query: query.data in dept_title)
def user_answer_dept(query):
    for i in range(len(dept_title)):
        if query.data == dept_title[i]:
            msg = dept_title[i]
            bot.answer_callback_query(query.id,"You Chose "+msg)
            bot.delete_message(users[query.from_user.id].user_id,users[query.from_user.id].message_id[3])
            get_add_info(query,msg)

