import time
from config import url
from bot import bot
from selenium.webdriver.common.by import By
from util.initiate_webdriver import initiate_driver
from selenium.common.exceptions import NoSuchElementException
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner
from util.useful_lists import master_check
count = 0

def driver_transfer():
    global page_to_scrape
    return page_to_scrape

def login(message):
    global page_to_scrape
    page_to_scrape = initiate_driver()
    page_to_scrape.get(url)
    master_check[0] = '1'
    # if count == 0:
    #     global page_to_scrape
    #     page_to_scrape = initiate_driver()
    #     try:
    #         page_to_scrape.get(url)
    #     except Exception:
    #         bot.send_message(message.chat.id,"Connection to the server timed out, plesase try again later")
    #         page_to_scrape.close()
    # try:
    #     page_to_scrape. find_element(
    #         By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
    #     sent_msgU = bot.send_message(message.chat.id, "Enter your username")
    #     bot.register_next_step_handler(sent_msgU, username_handler,sent_msgU)
    # except NoSuchElementException:
    #     bot.send_message(message.chat.id,"The website is under maintenance, please check back later")
    #     page_to_scrape.close()


def username_handler(message,sent_msgU):
    username = message.text
    cleaner(message)
    sent_msgP = "Now, Enter your password"
    bot.edit_message_text(sent_msgP,sent_msgU.chat.id,sent_msgU.message_id)
    bot.register_next_step_handler(sent_msgU,password_handler, username,sent_msgU)


def password_handler(message,username,sent_msgU):
    password = message.text
    cleaner(message)
    auth =  "Authenticating . . ."
    bot.edit_message_text(auth,sent_msgU.chat.id,sent_msgU.message_id)
    login_validator(message,username,password,sent_msgU)

def login_validator(message, usr, passd,sent_msgU):
    
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
    wrong_cred_handler(message, check_login,sent_msgU)


def wrong_cred_handler(message, c_login,sent_msgU):
    global count
    if (c_login != "People Online:"):
        # page_to_scrape.close()
        count+=1
        msg = "Login failed! Your Username or Password is incorrect, Please try again..."
        bot.edit_message_text(msg,sent_msgU.chat.id,sent_msgU.message_id)
        time.sleep(3)
        cleaner(sent_msgU)
        login(message)
    else:
        count = 0
        cleaner(sent_msgU)
        master_check[0] = '1'
        name = page_to_scrape.find_element(
            By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        msg = "Login Successful !!\nLogged in as: "+name
        bot.send_message(message.from_user.id, msg,reply_markup=buttons("s_login"))
