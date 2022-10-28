import time
from config import url
from bot import bot
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner
from util.interrupter import step_canceler
from util.user_database import users


def login(message):
    sent_msgW = bot.send_message(message.chat.id, "Please wait . . . ")
    if users[message.from_user.id].is_driver_opened == False:
        users[message.from_user.id].get_webdriver()
        print(users[message.from_user.id].first_name +" Webdriver Opened !!")
        try:
            users[message.from_user.id].driver.get(url)
        except Exception:
            sent_msgE = "Connection to the server timed out, plesase try again later"
            bot.edit_message_text(sent_msgE,sent_msgW.chat.id,sent_msgW.message_id)
            users[message.from_user.id].driver.close()
            print(users[message.from_user.id].first_name +" Webdriver Closed !!")
    try:
        users[message.from_user.id].driver.find_element(
            By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
        sent_msgU = "Enter your username"
        bot.edit_message_text(sent_msgU,sent_msgW.chat.id,sent_msgW.message_id)
        bot.register_next_step_handler(sent_msgW, username_handler,sent_msgW)
    except NoSuchElementException:
        sent_msgNS = "The website is under maintenance, please check back later"
        bot.edit_message_text(sent_msgNS,sent_msgW.chat.id,sent_msgW.message_id)
        users[message.from_user.id].driver.close()
        print(users[message.from_user.id].first_name +" Webdriver Closed !!")


def username_handler(message,sent_msgW):
    if message.text == '/x':
        step_canceler(message)
        users[message.from_user.id].driver.close()
        print(users[message.from_user.id].first_name +" Webdriver Closed !!")
    else: 
        username = message.text
        cleaner(message)
        sent_msgP = "Now, Enter your password"
        bot.edit_message_text(sent_msgP,sent_msgW.chat.id,sent_msgW.message_id)
        bot.register_next_step_handler(sent_msgW,password_handler, username,sent_msgW)


def password_handler(message,username,sent_msgW):
    if message.text == '/x':
        step_canceler(message)
        users[message.from_user.id].driver.close()
        print(users[message.from_user.id].first_name +" Webdriver Closed !!")
    else:
        password = message.text
        cleaner(message)
        auth =  "Authenticating . . ."
        bot.edit_message_text(auth,sent_msgW.chat.id,sent_msgW.message_id)
        login_validator(message,username,password,sent_msgW)

def login_validator(message, usr, passd,sent_msgW):
    
    usrname = users[message.from_user.id].driver.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
    passwd = users[message.from_user.id].driver.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")
    usrname.send_keys(usr)
    passwd.send_keys(passd)
    users[message.from_user.id].driver.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()

    check_login = users[message.from_user.id].driver.find_element(
        By.XPATH, "//div/table/tbody/tr/td[2]/span").text
    wrong_cred_handler(message, check_login,sent_msgW)


def wrong_cred_handler(message, c_login,sent_msgW):
    if (c_login != "People Online:"):
        users[message.from_user.id].is_driver_opened = True
        msg = "Login failed! Your Username or Password is incorrect, Please try again..."
        bot.edit_message_text(msg,sent_msgW.chat.id,sent_msgW.message_id)
        time.sleep(3)
        cleaner(sent_msgW)
        login(message)
    else:
        cleaner(sent_msgW)
        users[message.from_user.id].is_logged_in = True
        name = users[message.from_user.id].driver.find_element(
            By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        msg = "Login Successful !!\nLogged in as: " + name
        bot.send_message(message.from_user.id, msg,reply_markup=buttons("s_login"))
