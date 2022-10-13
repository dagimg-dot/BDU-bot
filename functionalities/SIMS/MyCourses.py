from bot import bot
from selenium.webdriver.common.by import By
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner
from util.useful_lists import cardinal_ordinal,OpenWeb,success_login

def All_Courses(message,sent_msg,web):
    try:
        if OpenWeb[success_login[0]] == 1:
            web.find_element(
                By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt62").click()

        courseTitle = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[3]/div/div[1]")
        credit_hour = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[4]/div/div[1]")
        dept = web.find_elements(
            By.XPATH, "//option")

        course_list = {}
        for i in range(len(courseTitle)):
            temp_data = {courseTitle[i].text: credit_hour[i].text}
            course_list.update(temp_data)

        full_str = "\n".join("{}\t\t{}".format(v, k)
                            for k, v in course_list.items())
        size = "There are " + str(len(courseTitle)-1) + \
            " courses in " + dept[0].text+" Department"
        full = full_str + "\n\n" + size
        bot.send_message(message.chat.id, full,reply_markup=buttons("my_courses"))
        cleaner(sent_msg)
    except Exception:
        sent_msg_error = "The database is being updated, please try agian later"
        bot.send_message(message.chat.id,sent_msg_error,reply_markup=buttons("my_courses"))
        cleaner(sent_msg)

def course_year_handler(message, choice,web,msg):

    year = message.text
    cleaner(message)
    if choice == 'y':
        semester = 0
        sent_msgC = "Checking availability . . ."
        bot.edit_message_text(sent_msgC,msg.chat.id,msg.message_id)
        course_validator(message, year, semester, choice,web,msg)
    elif choice == 's':
        sent_msgS ="Enter Semester"
        bot.edit_message_text(sent_msgS,msg.chat.id,msg.message_id)
        bot.register_next_step_handler(msg, course_semester_handler, year, choice,web,msg)


def course_semester_handler(message, year, choice,web,msg):
    semester = message.text
    cleaner(message)
    sent_msgC = "Checking availability . . ."
    bot.edit_message_text(sent_msgC,msg.chat.id,msg.message_id)
    course_validator(message, year, semester, choice,web,msg)


def course_validator(message, year, semester, choice,web,msg):
    try:
        if OpenWeb[success_login[0]] == 1:
            web.find_element(
                By.ID, "dnn_dnnTREEVIEW_ctldnnTREEVIEWt62").click()

        courseTitle = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[3]/div/div[1]")
        credit_hour = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[4]/div/div[1]")
        year1 = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[5]/div/div[1]")
        sem1 = web.find_elements(
            By.XPATH, "//div/table/tbody/tr/td[6]/div/div[1]")
        dept = web.find_elements(
            By.XPATH, "//option")

        years = []
        for i in range(1, len(year1)):
            years.append(year1[i].text)

        year_max = max(years)
        if choice == 'y':
            if year.isdigit() == False:
                sent_msgR = "Enter integers only. Please, Enter year again"
                bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
                bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
            elif int(year) > int(year_max):
                sent_msgR = dept[0].text+" is given in total of "+year_max+" years."+"\n"+"Please, Enter year again"
                bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
                bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
            else:
                course_list = {}
                for i in range(len(courseTitle)):
                    if year1[i].text == year:
                        temp_data = {courseTitle[i].text: credit_hour[i].text}
                        course_list.update(temp_data)

                year_sem1 = "These are the courses for "+ cardinal_ordinal[int(year)]+" year."
                full_str = "\n".join("{}\t\t{}".format(v, k)
                                    for k, v in course_list.items())
                full = year_sem1 + "\n\n" + full_str
                bot.send_message(message.chat.id, full,reply_markup=buttons("my_courses"))
                cleaner(msg)


        elif choice == 's':
            if year.isdigit() == False or semester.isdigit() == False:
                sent_msgR = "Enter integers only. Please, Enter year again"
                bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
                bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
            elif int(year) > int(year_max) and int(semester) > 2:
                sent_msgR = "Both your entries are wrong. Please, Enter year again"
                bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
                bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
            elif int(year) > int(year_max):
                sent_msgR = dept[0].text+" is given in total of "+year_max+" years."+"\n"+"Please, Enter year again"
                bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
                bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
            elif int(semester) > 2:
                sent_msgR = "There are only 2 semesters. Please, Enter semester again"
                bot.edit_message_text(sent_msgR,msg.chat.id,msg.message_id)
                bot.register_next_step_handler(msg, course_semester_handler, year, choice,web,msg)
            else:
                course_list = {}
                for i in range(len(courseTitle)):
                    if year1[i].text == year:
                        if sem1[i].text == semester:
                            temp_data = {courseTitle[i].text: credit_hour[i].text}
                            course_list.update(temp_data)
                year_sem2 = "These are the courses for "+ cardinal_ordinal[int(year)]+" year " + cardinal_ordinal[int(semester)] + " semester." 
                full_str = "\n".join("{}\t\t{}".format(v, k)
                                    for k, v in course_list.items())
                full = year_sem2 + "\n\n" + full_str
                bot.send_message(message.chat.id, full,reply_markup=buttons("my_courses"))
                cleaner(msg)
    except Exception:
        sent_msg_error = "The database is being updated, please try agian later"
        bot.send_message(message.chat.id, sent_msg_error,reply_markup=buttons("my_courses"))
        cleaner(msg)
