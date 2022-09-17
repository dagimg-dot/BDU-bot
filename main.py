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
url='https://studentinfo.bdu.edu.et/login.aspx?ReturnUrl=%2f'
page_to_scrape=webdriver.Edge()
page_to_scrape.minimize_window()
page_to_scrape.get(url)


@bot.message_handler(commands=[ 'start'])
def welcome(pm):
    msg=bot.send_message(pm.chat.id,"Hello "+str(pm.chat.username)+" This is BDU_SIMS Bot. It brings the Online Student Infomation of Bahir Dar University to telegram. Enjoy !!! \n\nTo see what it's capable of refer /help")
    bot.register_next_step_handler(msg, choice_handler)
    
@bot.message_handler(commands=[ 'actions'])
def choice_handler(pm):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Login')
    btn2 = types.KeyboardButton('Predict GPA')
    markup.add(btn1, btn2)
    msg=bot.send_message(pm.chat.id, "Choose what you want to do:" ,reply_markup=markup)
    bot.register_next_step_handler(msg, markup_handler)

def markup_handler(pm):
    if(pm.text == 'Login'):
        login(pm)
    # elif(pm.text == 'Predict GPA'):
        # msg=bot.send_message(pm.chat.id, "You Choose Predict GPA")
    

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
    bot.send_message(pm.chat.id, f"Username : {username}\nPassword: {password}")
    scrape_handler(pm,username,password)

def scrape_handler(pm,usr, passd):
    usrname=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
    passwd=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")
    usrname.send_keys(usr)
    passwd.send_keys(passd)
    page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()
    time.sleep(2)

    check_login=page_to_scrape.find_element(By.XPATH,"//div/table/tbody/tr/td[2]/span").text
    wrong_cred_handler(pm,check_login)

def wrong_cred_handler(pm,c_login):
    if(c_login!="People Online:"):
        msg="Login failed! Your Username or Password is incorrect, Please try again..."
        bot.send_message(pm.chat.id,msg)
        login(pm)
    else:   
        All_Grades_Extractor(pm)

def All_Grades_Extractor(pm):
        name=page_to_scrape.find_element(By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
        bot.send_message(pm.chat.id,"Logged in as: "+name+"\n")
        page_to_scrape.find_element(By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt63").click()


        courseTitle=page_to_scrape.find_elements(By.XPATH, "//div[1]/table/tbody/tr/td[2]/div")
        grade=page_to_scrape.find_elements(By.XPATH, "//div[1]/table/tbody/tr/td[4]/div")

        list_result=[]

        for i in range(len(courseTitle)):
            temp_data={'Course Title': courseTitle[i].text,
                    'Grade': grade[i].text}
            list_result.append(temp_data) 

        df_data=pd.DataFrame(list_result)
        bot.send_message(pm.chat.id,list_result)
        print(df_data)

bot.infinity_polling()