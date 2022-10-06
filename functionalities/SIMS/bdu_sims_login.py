
import time
from config import url
from bot import bot
from selenium.webdriver.common.by import By
from util.initiate_webdriver import initiate_driver
from selenium.common.exceptions import NoSuchElementException
from util.keyboard_buttons import buttons
from util.useful_lists import master_check

# length = len(master_check)
# if length != 1:
#     for i in master_check[:length-1]:
#         master_check.remove(i)

def login(message):
    page_to_scrape = initiate_driver()
    try:
        page_to_scrape.get(url)
    except Exception:
        bot.send_message(message.chat.id,"Connection to the server timed out, plesase try again later")
        page_to_scrape.close()
    try:
        # page_to_scrape. find_element(
        #     By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
        sent_msgU = bot.send_message(message.chat.id, "Enter your username")
        bot.register_next_step_handler(sent_msgU, username_handler,page_to_scrape,sent_msgU)
    except NoSuchElementException:
        bot.send_message(message.chat.id,"The website is under maintenance, please check back later")
        page_to_scrape.close()


def username_handler(message,page_to_scrape,sent_msgU):
    username = message.text
    bot.delete_message(message.chat.id,message.message_id)
    sent_msgP = "Enter your password"
    bot.edit_message_text(sent_msgP,sent_msgU.chat.id,sent_msgU.message_id)
    bot.register_next_step_handler(sent_msgU,password_handler, username,page_to_scrape,sent_msgU)


def password_handler(message,username,page_to_scrape,sent_msgU):
    password = message.text
    bot.delete_message(message.chat.id,message.message_id)
    auth =  "Authenticating . . ."
    bot.edit_message_text(auth,sent_msgU.chat.id,sent_msgU.message_id)
    login_validator(message,username,password,page_to_scrape,sent_msgU)

def login_validator(message, usr, passd,page_to_scrape,sent_msgU):
    
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
    wrong_cred_handler(message, check_login,page_to_scrape,sent_msgU)


def wrong_cred_handler(message, c_login,page_to_scrape,sent_msgU):
    if (c_login != "People Online:"):
        page_to_scrape.close()
        msg = "Login failed! Your Username or Password is incorrect, Please try again..."
        bot.edit_message_text(msg,sent_msgU.chat.id,sent_msgU.message_id)
        time.sleep(3)
        bot.delete_message(sent_msgU.chat.id,sent_msgU.message_id,timeout=3)
        login(message)
    else:
        bot.delete_message(sent_msgU.chat.id,sent_msgU.message_id,timeout=3)
        master_check[0] = '1'
        name = page_to_scrape.find_element(
            By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        msg = "Login Successful !!\nLogged in as: "+name
        bot.send_message(message.from_user.id, msg,reply_markup=buttons("s_login"))
