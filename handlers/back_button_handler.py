from bot import bot
from util.keyboard_buttons import buttons
from telebot import types
from util.useful_lists import master_check


def still_loggedin_checker(message):
    markup = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton('Yes', callback_data="Yes")
    no_btn = types.InlineKeyboardButton('No', callback_data="No")
    markup.add(yes_btn, no_btn)
    bot.send_message(message.chat.id, 'You are still Logged in. Do you want to log out ?', reply_markup=markup)

@bot.callback_query_handler(lambda query: query.data in ["Yes","No"])
def user_answer_logout(query):
    message = query.message
    if query.data == "Yes":
        # page_to_scrape.find_element(By.ID, "dnn_dnnLOGIN_cmdLogin").click()
        msg = "You are logged out !!"
        master_check[0] = '0'
        bot.answer_callback_query(query.id,msg)
        bot.send_message(message.chat.id, msg, reply_markup=buttons("Menu"))
        # bot.edit_message_reply_markup(message.chat.id,message.message_id,reply_markup=None)
    elif query.data == "No":
        bot.answer_callback_query(query.id,"Logging out Cancelled")
        # bot.edit_message_reply_markup(message.chat.id,message.message_id,reply_markup=None)
        # bot.send_message(message.chat.id, "Logging out Cancelled")