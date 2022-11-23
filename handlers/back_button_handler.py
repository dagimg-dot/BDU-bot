from bot import bot
from util.keyboard_buttons import buttons
from telebot import types
from util.state_holder import user_state_reset
from util.user_database import users


def still_loggedin_checker(message):
    users[message.from_user.id].message_id[0] = message.message_id
    markup = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton('Yes', callback_data="Yes")
    no_btn = types.InlineKeyboardButton('No', callback_data="No")
    markup.add(yes_btn, no_btn)
    sent_msg = bot.send_message(message.chat.id, 'You are still Logged in. Do you want to log out ?', reply_markup=markup)
    users[message.from_user.id].message_id[1] = sent_msg.message_id

@bot.callback_query_handler(lambda query: query.data in ["Yes","No"])
def user_answer_logout(query):
    if query.data == "Yes":
        users[query.from_user.id].driver.close()
        print(users[query.from_user.id].first_name +" Webdriver Closed !!")
        msg = "You are logged out !!"
        users[query.from_user.id].is_logged_in = False
        users[query.from_user.id].is_driver_opened = False
        user_state_reset(query)
        bot.answer_callback_query(query.id,msg,show_alert=True)
        bot.delete_message(query.from_user.id,users[query.from_user.id].message_id[1])
        bot.delete_message(query.from_user.id,users[query.from_user.id].message_id[0])
        bot.send_message(query.from_user.id, msg, reply_markup=buttons("Menu"))
    elif query.data == "No":
        bot.answer_callback_query(query.id,"Logging out Cancelled",show_alert=True)
        bot.delete_message(query.from_user.id,users[query.from_user.id].message_id[1])
        bot.delete_message(query.from_user.id,users[query.from_user.id].message_id[0])
