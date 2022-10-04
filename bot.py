from telebot import TeleBot
API_file = open('Token.txt', 'r')
API_TOKEN = API_file.read() 
API_file.close()

bot = TeleBot(API_TOKEN)

