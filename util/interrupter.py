from bot import bot


def step_canceler(message):
    bot.send_message(message.chat.id,"Request cancelled by user")
    bot.clear_step_handler(message)