from bot import bot
from util.keyboard_buttons import buttons
from telebot import types
from util.message_cleaner import cleaner
from util.state_holder import user_state_reset
from util.user_database import users


def still_loggedin_checker(message):
    global back 
    back = message
    markup = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton('Yes', callback_data="Yes")
    no_btn = types.InlineKeyboardButton('No', callback_data="No")
    markup.add(yes_btn, no_btn)
    global sent_msg 
    sent_msg = bot.send_message(message.chat.id, 'You are still Logged in. Do you want to log out ?', reply_markup=markup)

@bot.callback_query_handler(lambda query: query.data in ["Yes","No"])
def user_answer_logout(query):
    if query.data == "Yes":
        users[query.from_user.id].driver.close()
        print(users[back.from_user.id].first_name +" Webdriver Closed !!")
        msg = "You are logged out !!"
        users[query.from_user.id].is_logged_in = False
        users[query.from_user.id].is_driver_opened = False
        user_state_reset(back)
        bot.answer_callback_query(query.id,msg,show_alert=True)
        cleaner(sent_msg)
        cleaner(back)
        bot.send_message(query.from_user.id, msg, reply_markup=buttons("Menu"))
    elif query.data == "No":
        bot.answer_callback_query(query.id,"Logging out Cancelled",show_alert=True)
        cleaner(sent_msg)
        cleaner(back)