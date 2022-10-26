from bot import bot
from selenium.webdriver.common.by import By
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner
from util.useful_lists import success_login
from util.user_database import users,User

def My_Grades(message,sent_msg):
    try:
        if users[message.from_user.id].get_user_state()[success_login[2]] == 1:
            users[message.from_user.id].driver.find_element(
                By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt63").click()

        courseTitle = users[message.from_user.id].driver.find_elements(
            By.XPATH, "//div[1]/table/tbody/tr/td[2]/div")
        grade = users[message.from_user.id].driver.find_elements(
            By.XPATH, "//div[1]/table/tbody/tr/td[4]/div")

        grade_list = {}
        for i in range(1,len(courseTitle)):
            temp_data = {courseTitle[i].text: grade[i].text}
            grade_list.update(temp_data)
        if len(grade_list) != 0:
            full_str = "\n".join("{}\t\t{}".format(v, k)
                                for k, v in grade_list.items())
            bot.send_message(message.from_user.id, full_str,reply_markup=buttons("s_login"))
            cleaner(sent_msg)
        else: 
            bot.send_message(message.chat.id, "The database is being updated, please try agian later",reply_markup=buttons("my_status"))
            cleaner(sent_msg)
    except Exception:
        sent_msg_error = "Request to the server timed out. Please try again later"
        bot.send_message(message.chat.id,sent_msg_error,reply_markup=buttons("s_login"))
        cleaner(sent_msg)