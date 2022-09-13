from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

url='https://studentinfo.bdu.edu.et/login.aspx?ReturnUrl=%2f'
page_to_scrape=webdriver.Edge()
page_to_scrape.get(url)
#page_to_scrape.maximize_window()

username=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
password=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")

usrname=input("Enter your username please: ")
username.send_keys(usrname)
passwd=input("Ener your password please: ")
password.send_keys(passwd)

page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_cmdLogin").click()
time.sleep(2)

check_login=page_to_scrape.find_element(By.XPATH,"//div/table/tbody/tr/td[2]/span").text
while(check_login!="People Online:"):
    page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername").clear()
    username=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtUsername")
    password=page_to_scrape.find_element(By.ID, "dnn_ctr_Login_Login_DNN_txtPassword")
    
    print("Login failed. Please try again...")
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

