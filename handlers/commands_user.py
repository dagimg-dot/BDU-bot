from telebot import TeleBot
from telebot.types import Message
from telebot import formatting
from util.keyboard_buttons import buttons
from util.user_database import collection, users, User


# For '/start' command
def start_message(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    u_id = collection.find_one({"_id": user_id})
    if u_id == None:
        NewUser = User(user_id, f_name)
        temp_user = {user_id: NewUser}
        users.update(temp_user)
        NewUserDB = {"_id": user_id, "f_name": f_name}
        collection.insert_one(NewUserDB)
        start_new = f"Hello {f_name}. Welcome to BDU-SIMS Bot. It brings you the Online Student Infomation of Bahir Dar University to telegram. Enjoy !!! \n\nTo start using the bot /menu \nTo see what it's capable of refer /help (recommended)"
        bot.send_message(user_id, start_new)
        print(users[user_id].first_name + "started using the bot")
    else:
        start_old = f"Welcome back {f_name}. This is BDU-SIMS Bot. It brings you the Online Student Infomation of Bahir Dar University to telegram. Enjoy !!! \n\nTo start using the bot /menu \nTo see what it's capable of refer /help (recommended)"
        bot.send_message(user_id, start_old)


# For '/help' command
def help_message(message: Message, bot: TeleBot):
    f_name = message.from_user.first_name
    bot.send_message(
        message.chat.id, f"What's good " + formatting.hbold(f_name)+" !! This bot includes all the functionalities of the BDU SIMS website. You can access your . . .\n\n-> Courses \n-> Grades \n-> Status (GPAs) \n\nAnd also you can calculate your GPA using the built-in  GPA Calculator.\n\nTo "+formatting.hbold('access your account')+", you need to "+formatting.hbold('login')+". Just press the /menu command then press Login and you will be asked to enter your credentials, after that everything will be as easy as abc...\n\nThe "+formatting.hbold('Predict GPA')+" button gives you access to the built-in GPA Calculator. After you choose your department it automatically fetches the courses  divided in semesters for you so you are not expected to remember.\n\nTo cancel any request from the bot (E.G: when you are asked to enter something) just send '/x'.\n\n    ---- Have fun with the bot ---- \n\nIf you are a little worried about your privacy, I got u. Check out the source code on "+formatting.hlink('github', 'https://github.com/dagimg-dot')+". It's an open source project.", parse_mode='HTML', disable_web_page_preview=True)


# For '/menu' command
def menu_handler(message: Message, bot: TeleBot):
    msg = "Main Menu"
    bot.send_message(message.chat.id, msg, reply_markup=buttons())
