from bot import bot


def step_canceler(message):
    bot.send_message(message.chat.id,"❌Request to the server cancelled by the user❌")
    bot.clear_step_handler(message)