import telebot

API_file = open('API.txt', 'r')
API_TOKEN = API_file.read()
API_file.close()

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def welcome(pm):
    sent_msg = bot.send_message(pm.chat.id, "What is your username?")
    bot.register_next_step_handler(sent_msg, username_handler) #Next message will call the name_handler function
    
def username_handler(pm):
    username = pm.text
    sent_msg = bot.send_message(pm.chat.id, "What is your password?")
    bot.register_next_step_handler(sent_msg, password_handler, username) #Next message will call the age_handler function

def password_handler(pm, username):
    password = pm.text
    bot.send_message(pm.chat.id, f"Username : {username}\nPassword: {password}.")
    bot.register_next_step_handler(send_credentials,username,password)

def send_credentials(username,password):
    usr=username
    passwd=password
    return usr,passwd
    

bot.polling()