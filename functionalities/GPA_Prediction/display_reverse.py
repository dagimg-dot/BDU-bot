from bot import bot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from util.user_database import users


def state_identifier(message):
    for i in range(5):
        if users[message.from_user.id].get_rev_state(i) == 1:
            return i


def state_modifier(query, current_state, data):
    if data == "n":
        users[query.from_user.id].set_rev_state(current_state + 1, 1)
        users[query.from_user.id].set_rev_state(current_state, 0)
    elif data == "p":
        users[query.from_user.id].set_rev_state(current_state - 1, 1)
        users[query.from_user.id].set_rev_state(current_state, 0)


def display_final(message):
    users[message.from_user.id].current_state = state_identifier(message)
    prev_button = InlineKeyboardButton("⬅️ Prev", callback_data="p")
    next_button = InlineKeyboardButton("Next ➡️", callback_data="n")
    full_str = str(users[message.from_user.id].current_state + 1) + " out of 5" + "  GPA:  " + str(round(users[message.from_user.id].gpa_list[users[message.from_user.id].current_state], 3)) + "\n\n" + "\n".join("{}  {}".format(v, k) for k, v in users[message.from_user.id].possibility_dict[users[message.from_user.id].current_state].items())
    main_msg = bot.send_message(message.from_user.id, full_str,
                                reply_markup=InlineKeyboardMarkup().row(prev_button, next_button))
    users[message.from_user.id].message_id[2] = main_msg.message_id


@bot.callback_query_handler(lambda query: query.data in ["p", "n"])
def rotate_prediction(query):
    if query.data == "p":
        if users[query.from_user.id].current_state == 0:
            bot.answer_callback_query(
                query.id, "⚠️  Start of list  ⚠️", show_alert=True)
        else:
            state_modifier(
                query, users[query.from_user.id].current_state, query.data)
            users[query.from_user.id].current_state = state_identifier(query)
            prev_button = InlineKeyboardButton("⬅️ Prev", callback_data="p")
            next_button = InlineKeyboardButton("Next ➡️", callback_data="n")
            full_str = str(users[query.from_user.id].current_state + 1) + " out of 5" + "  GPA:  " + str(round(users[query.from_user.id].gpa_list[users[query.from_user.id].current_state], 3)) + "\n\n" + "\n".join("{}  {}".format(v, k)
                                                                                                                                                                                                                     for k, v in users[query.from_user.id].possibility_dict[users[query.from_user.id].current_state].items())
            bot.edit_message_text(full_str, users[query.from_user.id].user_id, users[query.from_user.id].message_id[2],
                                  reply_markup=InlineKeyboardMarkup().row(prev_button, next_button))
    elif query.data == "n":
        if users[query.from_user.id].current_state == 4:
            bot.answer_callback_query(
                query.id, "⚠️  End of list  ⚠️", show_alert=True)
        else:
            state_modifier(
                query, users[query.from_user.id].current_state, query.data)
            users[query.from_user.id].current_state = state_identifier(query)
            prev_button = InlineKeyboardButton("⬅️ Prev", callback_data="p")
            next_button = InlineKeyboardButton("Next ➡️", callback_data="n")
            full_str = str(users[query.from_user.id].current_state + 1) + " out of 5" + "  GPA:  " + str(round(users[query.from_user.id].gpa_list[users[query.from_user.id].current_state], 3)) + "\n\n" + "\n".join("{}  {}".format(v, k)
                                                                                                                                                                                                                     for k, v in users[query.from_user.id].possibility_dict[users[query.from_user.id].current_state].items())
            bot.edit_message_text(full_str, users[query.from_user.id].user_id, users[query.from_user.id].message_id[2],
                                  reply_markup=InlineKeyboardMarkup().row(prev_button, next_button))
