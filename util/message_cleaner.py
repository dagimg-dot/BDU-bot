from bot import bot



def cleaner(message):
    bot.delete_message(message.chat.id,message.message_id)