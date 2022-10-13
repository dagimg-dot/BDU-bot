from bot import bot
from selenium.webdriver.common.by import By
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner
from util.useful_lists import cardinal_ordinal,OpenWeb,success_login
import time


def current_cgpa(message,web):
    try:
        if OpenWeb[success_login[1]] == 1:
            web.find_element(
                By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt64").click()

        cgpa = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[11]/div/div[1]")
        year_status = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[4]/div/div[1]")
        years = []
        for i in range(1, len(year_status)):
            years.append(year_status[i].text)

        year_max = max(years)
        
        for i in range(len(year_status)):
            if year_status[i].text == year_max:
                c_gpa = cgpa[i].text

        if c_gpa == "":
            bot.send_message(message.chat.id, "Your current CGPA is not known")
        else:
            msg = "Your current CGPA is "+c_gpa
            bot.send_message(message.chat.id, msg)
    except Exception:
        bot.send_message(message.chat.id,"The database is being updated, please try again later")


def sgpa_year_handler(message,web,msg):
    year = message.text
    cleaner(message)
    sent_msgS = "Enter semester"
    bot.edit_message_text(sent_msgS,msg.chat.id,msg.message_id)
    bot.register_next_step_handler(msg, sgpa_semester_handler, year,web,msg)


def sgpa_semester_handler(message, year,web,msg):
    semester = message.text
    cleaner(message)
    sent_msgC = "Checking availability . . ."
    bot.edit_message_text(sent_msgC,msg.chat.id,msg.message_id)
    sgpa_validator(message, year, semester,web,msg)
    

def sgpa_validator(message, year, semester,web,msg):
    try:
        if OpenWeb[success_login[1]] == 1:
            web.find_element(
                By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt64").click()

        year_status = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[4]/div/div[1]")
        sem_status = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[5]/div/div[1]")
        sgpa = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[10]/div/div[1]")
        years = []
        for i in range(1, len(year_status)):
            years.append(year_status[i].text)

        year_max = max(years)

        if year.isdigit() == False or semester.isdigit() == False:
            sent_msgR = "Enter integers only. Please, Enter year again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgpa_year_handler, web,msg)
        elif int(year) > int(year_max) and int(semester) > 2:
            sent_msgR = "Both your entries are wrong. Please, Enter year again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgpa_year_handler,web,msg)
        elif int(year) > int(year_max):
            sent_msgR = "You didn't get there. Please, Enter year again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgpa_year_handler,web,msg)
        elif int(semester) > 2:
            sent_msgR = "There are only 2 semesters. Please, Enter semester again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgpa_semester_handler, year,web,msg)
        else:
            for i in range(len(year_status)):
                if year_status[i].text == year:
                    if sem_status[i].text == semester:
                        sem_gpa = sgpa[i].text
            full_str = "Your GPA in " + \
                cardinal_ordinal[int(
                    year)]+" year "+cardinal_ordinal[int(semester)]+" semester" + " is "+sem_gpa
            bot.send_message(message.chat.id, full_str,reply_markup=buttons("my_status"))
            cleaner(msg)
    except Exception:
        sent_msg_error = "The database is being updated, please try agian later"
        bot.send_message(message.chat.id, sent_msg_error,reply_markup=buttons("my_status"))
        cleaner(msg)

def sgrade_year_handler(message,web,msg):
    year = message.text
    cleaner(message)
    sent_msgS = "Enter semester"
    bot.edit_message_text(sent_msgS,msg.chat.id,msg.message_id)
    bot.register_next_step_handler(msg, sgrade_semester_handler, year,web,msg)


def sgrade_semester_handler(message, year,web,msg):
    semester = message.text
    cleaner(message)
    sent_msgC = "Checking availability . . ."
    bot.edit_message_text(sent_msgC,msg.chat.id,msg.message_id)
    sgrade_validator(message, year, semester,web,msg)


def sgrade_validator(message, year, semester,web,msg):
    try:
        web.find_element(
            By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt64").click()
        year_status = web.find_elements(
        By.XPATH, "//div/table/tbody/tr/td[4]/div/div[1]")
        sem_status = web.find_elements(
        By.XPATH, "//div/table/tbody/tr/td[5]/div/div[1]")

        years = []
        for i in range(1, len(year_status)):
            years.append(year_status[i].text)

        year_max = max(years)
        if year.isdigit() == False or semester.isdigit() == False:
            sent_msgR = "Enter integers only. Please, Enter year again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgrade_year_handler, web,msg)
        elif int(year) > int(year_max) and int(semester) > 2:
            sent_msgR = "Both your entries are wrong. Please, Enter year again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgrade_year_handler,web,msg)
        elif int(year) > int(year_max):
            sent_msgR = "You didn't get there. Please, Enter year again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgrade_year_handler,web,msg)
        elif int(semester) > 2:
            sent_msgR = "There are only 2 semesters. Please, Enter semester again"
            bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
            bot.register_next_step_handler(msg, sgrade_semester_handler, year,web,msg)
        else:
            grade_list = {}
            for i in range(len(year_status)):
                if year_status[i].text == year:
                    if sem_status[i].text == semester:
                        toggle = 2*i-1
                        web.find_element(By.CSS_SELECTOR, "tr:nth-child("+str(
                            toggle)+") > td.ob_gDGE.ob_gC.ob_gC_Fc > div > div.ob_gDGEB > img").click()
                        time.sleep(3)
                        title = web.find_elements(
                            By.XPATH, "//div/table/tbody/tr/td[4]/div/div[1]")
                        grade = web.find_elements(
                            By.XPATH, "//div/table/tbody/tr/td[6]/div[1]")
                        len_title = len(title)
                        for i in range(len(title)):
                            if title[i].text == "Title":
                                j = i
                                break
                        for i in range(j, len(title)):
                            if title[i].text in years:
                                len_title -= 1
                        for i in range(j, len_title):
                            temp_data = {title[i].text: grade[i].text}
                            grade_list.update(temp_data)
                        
            full_str = "\n".join("{}  {}".format(v, k)
                                    for k, v in grade_list.items())
            bot.send_message(message.chat.id, full_str,reply_markup=buttons("my_status"))
            cleaner(msg)
            web.find_element(
                By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt64").click()
    except Exception:
        sent_msg_error = "The database is being updated, please try agian later"
        bot.send_message(message.chat.id, sent_msg_error,reply_markup=buttons("my_status"))
        cleaner(msg)