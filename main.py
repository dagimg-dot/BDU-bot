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


@bot.message_handler(commands=['start'])
def welcome(pm):
    msg = bot.send_message(pm.chat.id, "Hello "+str(pm.chat.username) +
                           " This is BDU_SIMS Bot. It brings the Online Student Infomation of Bahir Dar University to telegram. Enjoy !!! \n\nTo see what it's capable of refer /help")
    bot.register_next_step_handler(msg, choice_handler)


@bot.message_handler(commands=['actions'])
def choice_handler(pm):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Login')
    btn2 = types.KeyboardButton('Predict GPA')
    # if(callback_inline(pm,call)==False):
    #     btn3 = types.KeyboardButton('Login as')
    #     markup.add(btn1, btn2, btn3)
    # else:
    markup.add(btn1, btn2)
        
    msg = bot.send_message(
        pm.chat.id, "Choose what you want to do:", reply_markup=markup)
    bot.register_next_step_handler(msg, markup_handler)


def markup_handler(pm):
    if (pm.text == 'Login'):
        login(pm)
    elif(pm.text == 'Predict GPA'):
        msg="You Choose Predict GPA"
        bot.send_message(pm.chat.id,msg)

def login(pm):
    page_to_scrape. find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
    sent_msg = bot.send_message(pm.chat.id, "Enter your username")
    bot.register_next_step_handler(sent_msg, username_handler)


def username_handler(pm):
    username = pm.text
    sent_msg = bot.send_message(pm.chat.id, "Enter your password")
    bot.register_next_step_handler(sent_msg, password_handler, username)


def password_handler(pm, username):
    password = pm.text
    bot.send_message(
        pm.chat.id, f"Username : {username}\nPassword: {password}")
    login_validator(pm, username, password)


def login_validator(pm, usr, passd):
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
    wrong_cred_handler(pm, check_login)


def wrong_cred_handler(pm, c_login):
    if (c_login != "People Online:"):
        msg = "Login failed! Your Username or Password is incorrect, Please try again..."
        bot.send_message(pm.chat.id, msg)
        login(pm)
    else:
        time.sleep(2)
        name=page_to_scrape.find_element(By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        msg="Logged in as: "+name+"\n"
        bot.send_message(pm.chat.id,msg)
        choice_handler_login(pm)


def choice_handler_login(pm):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('My Courses')
    btn2 = types.KeyboardButton('My Status')
    btn3 = types.KeyboardButton('My Grades')
    btn4 = types.KeyboardButton('My Dormitory')
    btn5 = types.KeyboardButton('🔙Back')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    msg = bot.send_message(pm.chat.id, "Choose what you want to do:", reply_markup=markup)
    bot.register_next_step_handler(msg, markup_handler_login)


def markup_handler_login(pm):
    if (pm.text == 'My Courses'):
       My_Courses(pm)
    elif (pm.text == 'My Status'):
        My_Status(pm)
    elif (pm.text == 'My Grades'):
        My_Grades(pm)
    elif (pm.text == 'My Dormitory'):
        My_Dormitory(pm)
    elif (pm.text == '🔙Back'):
        still_loggedin_checker(pm)

def still_loggedin_checker(pm):
    markup=types.InlineKeyboardMarkup()
    button=types.InlineKeyboardButton('Yes',callback_data="y")
    button2=types.InlineKeyboardButton('No',callback_data="n")
    markup.add(button,button2)
    bot.send_message(pm.chat.id,'You are still Logged in. Do you want to log out ?',reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):
    choice=False
    if call.data == "y":
        page_to_scrape.find_element(By.ID, "dnn_dnnLOGIN_cmdLogin").click()
        page_to_scrape.close()
        choice_handler(call)
        choice=True
    # elif call.data == "n":
    #     choice_handler(pm)
    # return choice
        


def My_Courses(pm):
    msg="My Courses"
    bot.send_message(pm.chat.id,msg)

def My_Status(pm):
    msg="My Status"
    bot.send_message(pm.chat.id,msg)

def My_Grades(pm):
    name = page_to_scrape.find_element(
        By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
    bot.send_message(pm.chat.id, "Logged in as: "+name+"\n")
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

    df_data = pd.DataFrame(list_result)
    bot.send_message(pm.chat.id, list_result)
    print(df_data)

def My_Dormitory(pm):
    msg="My Dromitory"
    bot.send_message(pm.chat.id,msg)

bot.infinity_polling()
