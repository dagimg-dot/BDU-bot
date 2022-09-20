from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import telebot
from telebot import types



API_file = open('Token.txt', 'r')
API_TOKEN = API_file.read()
API_file.close()

bot = telebot.TeleBot(API_TOKEN)
print("Bot started ...")
url = 'https://studentinfo.bdu.edu.et/login.aspx?ReturnUrl=%2f'
page_to_scrape = webdriver.Edge()
page_to_scrape.minimize_window()
page_to_scrape.get(url)

menu = ["Login", "Predict GPA"]
success_login = ["My Courses", "My Status", "My Grades", "My Dormitory"]
MyC = ["All Courses", "Courses given on a specific year",
       "Courses given on a specific semester"]
MyS = ["Cumulative GPA - CGPA", "Semester GPA - SGPA", "Semester Grades"]

buttons_clicked = []

def buttons(type="Menu"):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if type == "Menu":
        row = [types.KeyboardButton(x) for x in menu]
        markup.add(*row)
    elif type == "s_login":
        row = [types.KeyboardButton(x) for x in success_login]
        markup.add(*row)
        markup.add(types.KeyboardButton("Back to Menu"))
    elif type == "my_courses":
        markup.row_width = 1
        row = [types.KeyboardButton(x) for x in MyC]
        markup.add(*row)
        markup.add(types.KeyboardButton("Back"),
                   types.KeyboardButton("Back to Menu"))
    elif type == "my_status":
        markup.row_width = 1
        row = [types.KeyboardButton(x) for x in MyS]
        markup.add(*row)
        markup.add(types.KeyboardButton("Back"),
                   types.KeyboardButton("Back to Menu"))
    return markup

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id, f"Hello {message.from_user.first_name}. This is BDU_SIMS Bot. It brings the Online Student Infomation of Bahir Dar University to telegram. Enjoy !!! \n\nTo start using the bot /menu \nTo see what it's capable of refer /help")


@bot.message_handler(commands=["menu"])
def menu_handler(message):
    msg = "Main Menu"
    bot.send_message(message.chat.id, msg, reply_markup=buttons())

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    if message.text == menu[0]:
        buttons_clicked.append(message.text)
        login(message)
    elif message.text == menu[1]:
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "GPA Prediction Tool",
                         reply_markup=markup)
    elif message.text == success_login[0]:
        buttons_clicked.append(message.text)
        bot.send_message(message.from_user.id, success_login[0],
                         reply_markup=buttons("my_courses"))
    elif message.text == success_login[1]:
        buttons_clicked.append(message.text)
        bot.send_message(message.from_user.id, success_login[1],
                         reply_markup=buttons("my_status"))
    elif message.text == success_login[2]:
        bot.send_message(message.from_user.id, "Pulling Grades ... ",
                         reply_markup=buttons("s_login"))
        My_Grades(message)
    elif message.text == success_login[3]:
        bot.send_message(message.from_user.id, success_login[3],
                         reply_markup=buttons("s_login"))
    elif message.text == MyC[0]:
        bot.send_message(message.from_user.id, MyC[0],
                         reply_markup=buttons("my_courses"))
    elif message.text == MyC[1]:
        bot.send_message(message.from_user.id, MyC[1],
                         reply_markup=buttons("my_courses"))
    elif message.text == MyC[2]:
        bot.send_message(message.from_user.id, MyC[2],
                         reply_markup=buttons("my_courses"))
    elif message.text == MyS[0]:
        bot.send_message(message.from_user.id, MyS[0],
                         reply_markup=buttons("my_status"))
    elif message.text == MyS[1]:
        bot.send_message(message.from_user.id, MyS[1],
                         reply_markup=buttons("my_status"))
    elif message.text == MyS[2]:
        bot.send_message(message.from_user.id, MyS[2],
                         reply_markup=buttons("my_status"))
    elif message.text == "Back":
        back_button_handler(message)
    elif message.text == "Back to Menu":
        still_loggedin_checker(message)
    else:
        bot.send_message(message.from_user.id, "I didn't get what you say ...")


def back_button_handler(message):
    length=len(buttons_clicked)
    if length !=1:
        for i in buttons_clicked[:length-1]:
            buttons_clicked.remove(i)
    if buttons_clicked[0] == "My Courses" or buttons_clicked[0] == "My Status":
        bot.send_message(message.from_user.id,"Back",reply_markup=buttons("s_login"))
    elif buttons_clicked[0] == "Login":
        bot.send_message(message.chat.id,"Back",reply_markup=buttons("Menu"))

def login(message):
    page_to_scrape.get(url)
    page_to_scrape. find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
    sent_msg = bot.send_message(message.chat.id, "Enter your username")
    bot.register_next_step_handler(sent_msg, username_handler)


def username_handler(message):
    username = message.text
    sent_msg = bot.send_message(message.chat.id, "Enter your password")
    bot.register_next_step_handler(sent_msg, password_handler, username)


def password_handler(message, username):
    password = message.text
    bot.send_message(
        message.chat.id, f"Username : {username}\nPassword: {password}")
    login_validator(message, username, password)


def login_validator(message, usr, passd):
    usrname = page_to_scrape.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
    passwd = page_to_scrape.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")
    usrname.send_keys(usr)
    passwd.send_keys(passd)
    page_to_scrape.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()
    time.sleep(2)

    check_login = page_to_scrape.find_element(
        By.XPATH, "//div/table/tbody/tr/td[2]/span").text
    wrong_cred_handler(message, check_login)


def wrong_cred_handler(message, c_login):
    if (c_login != "People Online:"):
        msg = "Login failed! Your Username or Password is incorrect, Please try again..."
        bot.send_message(message.chat.id, msg)
        login(message)
    else:
        name=page_to_scrape.find_element(By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        msg="Login Successful !!\nLogged in as: "+name
        bot.send_message(message.from_user.id, msg,
                         reply_markup=buttons("s_login"))


def still_loggedin_checker(message):
    markup=types.InlineKeyboardMarkup()
    button=types.InlineKeyboardButton('Yes',callback_data="y")
    button2=types.InlineKeyboardButton('No',callback_data="n")
    markup.add(button,button2)
    bot.send_message(message.chat.id,'You are still Logged in. Do you want to log out ?',reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):
    message=call.message
    if call.data == "y":
        page_to_scrape.find_element(By.ID, "dnn_dnnLOGIN_cmdLogin").click()
        msg="You are logged out !!"
        bot.send_message(message.chat.id,msg,reply_markup=buttons("Menu"))
    elif call.data == "n":
        bot.send_message(message.chat.id,"Logging out Cancelled")

def My_Courses(message):
    msg="My Courses option"
    bot.send_message(message.chat.id,msg)

def My_Status(message):
    msg="My Status option"
    bot.send_message(message.chat.id,msg)

def My_Grades(message):
    page_to_scrape.find_element(
        By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt63").click()

    courseTitle = page_to_scrape.find_elements(
        By.XPATH, "//div[1]/table/tbody/tr/td[2]/div")
    grade = page_to_scrape.find_elements(
        By.XPATH, "//div[1]/table/tbody/tr/td[4]/div")

    list_result = []

    for i in range(len(courseTitle)):
        temp_data = {'Course Title': courseTitle[i].text,
                     'Grade': grade[i].text}
        list_result.append(temp_data)

    # for i in list_result:
    #     print(i)
    df_data = pd.DataFrame(list_result)
    bot.send_message(message.chat.id, df_data)
    # print(df_data)
    # msg="My Grades option"
    # bot.send_message(message.chat.id,msg)

def My_Dormitory(message):
    msg="My Dromitory option"
    bot.send_message(message.chat.id,msg)

bot.infinity_polling()
