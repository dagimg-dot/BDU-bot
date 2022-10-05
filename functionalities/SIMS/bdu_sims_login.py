
from config import url
from bot import bot
from selenium.webdriver.common.by import By
from util.initiate_webdriver import initiate_driver
from selenium.common.exceptions import NoSuchElementException
from util.keyboard_buttons import buttons
from util.useful_lists import master_check



def login(message):
    page_to_scrape = initiate_driver()
    try:
        page_to_scrape.get(url)
    except Exception:
        bot.send_message(message.chat.id,"Connection to the server timed out, plesase try again later")
        page_to_scrape.close()
    try:
        page_to_scrape. find_element(
            By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
        sent_msg = bot.send_message(message.chat.id, "Enter your username")
        bot.register_next_step_handler(sent_msg, username_handler,page_to_scrape)
    except NoSuchElementException:
        bot.send_message(message.chat.id,"The website is under maintenance, please check back later")
        page_to_scrape.close()


def username_handler(message,page_to_scrape):
    username = message.text
    sent_msg = bot.send_message(message.chat.id, "Enter your password")
    bot.register_next_step_handler(sent_msg, password_handler, username,page_to_scrape)


def password_handler(message, username,page_to_scrape):
    password = message.text
    bot.send_message(
        message.chat.id, "Authenticating . . .")
    login_validator(message, username, password,page_to_scrape)

def login_validator(message, usr, passd,page_to_scrape):
    
    usrname = page_to_scrape.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
    passwd = page_to_scrape.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")
    usrname.send_keys(usr)
    passwd.send_keys(passd)
    page_to_scrape.find_element(
        By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()

    check_login = page_to_scrape.find_element(
        By.XPATH, "//div/table/tbody/tr/td[2]/span").text
    wrong_cred_handler(message, check_login,page_to_scrape)


def wrong_cred_handler(message, c_login,page_to_scrape):
    if (c_login != "People Online:"):
        msg = "Login failed! Your Username or Password is incorrect, Please try again..."
        # bot.edit_message_text(msg,message.chat.id,message.message_id,)
        bot.send_message(message.chat.id, msg)
        login(message)
    else:
        master_check.append('1')
        name = page_to_scrape.find_element(
            By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        msg = "Login Successful !!\nLogged in as: "+name
        bot.send_message(message.from_user.id, msg,
                         reply_markup=buttons("s_login"))
        # login_check(master_check)
