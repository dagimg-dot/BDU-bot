from telebot import TeleBot
# API_file = open('Token.txt', 'r')
# API_TOKEN = API_file.read() 
# API_file.close()

from config import TG_BOT_TOKEN
bot = TeleBot(TG_BOT_TOKEN)

