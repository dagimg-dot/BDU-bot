from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
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
    # scraperBDU.credentials(username)
    sent_msg = bot.send_message(pm.chat.id, "What is your password?")
    bot.register_next_step_handler(sent_msg, password_handler, username) #Next message will call the age_handler function

def password_handler(pm, username):
    password = pm.text
    # scraperBDU.credentials(password)
    bot.send_message(pm.chat.id, f"Username : {username}\nPassword: {password}")
    #bot.register_next_step_handler(sent_msg,scrape_handler,username,password)
    scrape_handler(username,password)

# def send_credentials(username, password):
#     usrname.send_keys(username)
#     passwd.send_keys(password)

# async def send_credentials(username, password):
#     # username.send_keys(usr)
#     # password.send_keys(passwd)
#     usr=username
#     passwd=password
#     return usr,passwd

def scrape_handler(usr, passd):
    url='https://studentinfo.bdu.edu.et/login.aspx?ReturnUrl=%2f'
    page_to_scrape=webdriver.Edge()
    page_to_scrape.get(url)
    page_to_scrape.minimize_window()

    usrname=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
    passwd=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")




    # usr,passwd=send_credentials()
    usrname.send_keys(usr)
    passwd.send_keys(passd)

    # def credentials(cred):
    #     if "BDU" in cred:
    #         username.send_keys(cred)
    #     else:
    #         password.send_keys(cred)

    page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()
    time.sleep(2)

    check_login=page_to_scrape.find_element(By.XPATH,"//div/table/tbody/tr/td[2]/span").text
    while(check_login!="People Online:"):
        page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
        username=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
        password=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")
        
        bot.send_message("Login failed. Please try again...")
        # print("Login failed. Please try again...")
        usrname=input("Enter your username please: ")
        username.send_keys(usrname)
        passwd=input("Ener your password please: ")
        password.send_keys(passwd)
        
        page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()
        time.sleep(2)
        
        check_login=page_to_scrape.find_element(By.XPATH,"//div/table/tbody/tr/td[2]/span").text


    name=page_to_scrape.find_element(By.XPATH, "//table[2]/tbody/tr/td[3]/a[1]").text
    print("Logged in as: "+name+"\n")
    page_to_scrape.find_element(By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt63").click()


    courseTitle=page_to_scrape.find_elements(By.XPATH, "//div[1]/table/tbody/tr/td[2]/div")
    grade=page_to_scrape.find_elements(By.XPATH, "//div[1]/table/tbody/tr/td[4]/div")

    list_result=[]

    for i in range(len(courseTitle)):
        temp_data={'Course Title': courseTitle[i].text,
                'Grade': grade[i].text}
        list_result.append(temp_data) 

    df_data=pd.DataFrame(list_result)
    print(df_data)

bot.polling()