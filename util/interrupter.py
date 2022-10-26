from bot import bot


def step_canceler(message):
    bot.send_message(message.chat.id,"✅The operation has been cancelled by the user")
    bot.clear_step_handler(message)