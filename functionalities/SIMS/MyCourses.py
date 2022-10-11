from bot import bot
from selenium.webdriver.common.by import By
from util.keyboard_buttons import buttons
from util.message_cleaner import cleaner


# web = driver_transfer()

def All_Courses(message,sent_msg,web):
    try:
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

def course_year_handler(message, choice,web):
    year = message.text

    if choice == 'y':
        semester = 0
        bot.send_message(message.chat.id, "Checking availability . . .")
        course_validator(message, year, semester, choice,web)
    elif choice == 's':
        sent_msg = bot.send_message(message.chat.id, "Enter Semester")
        bot.register_next_step_handler(
            sent_msg, course_semester_handler, year, choice,web)


def course_semester_handler(message, year, choice,web):
    semester = message.text
    bot.send_message(
        message.chat.id, "Checking availability . . .")
    course_validator(message, year, semester, choice,web)


def course_validator(message, year, semester, choice,web):
    try:
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
                msg = bot.send_message(message.chat.id, "Enter integers only. Please, Enter year again")
                bot.register_next_step_handler(msg, course_year_handler, choice)
            elif int(year) > int(year_max):
                bot.send_message(
                    message.chat.id, dept[0].text+" is given in total of "+year_max+" years.")
                msg = bot.send_message(message.chat.id, "Please, Enter year again")
                bot.register_next_step_handler(msg, course_year_handler, choice)
            else:
                course_list = {}
                for i in range(len(courseTitle)):
                    if year1[i].text == year:
                        temp_data = {courseTitle[i].text: credit_hour[i].text}
                        course_list.update(temp_data)

                full_str = "\n".join("{}\t\t{}".format(v, k)
                                    for k, v in course_list.items())
                bot.send_message(message.chat.id, full_str)

        elif choice == 's':
            if year.isdigit() == False or semester.isdigit() == False:
                msg = bot.send_message(message.chat.id, "Enter integers only. Please, Enter year again")
                bot.register_next_step_handler(msg, course_year_handler, choice)
            elif int(year) > int(year_max) and int(semester) > 2:
                bot.send_message(
                    message.chat.id, "Both your entries are wrong. Please start again")
                msg = bot.send_message(message.chat.id, "Please, Enter year again")
                bot.register_next_step_handler(msg, course_year_handler, choice)
            elif int(year) > int(year_max):
                bot.send_message(
                    message.chat.id, dept[0].text+" is given in total of "+year_max+" years.")
                msg = bot.send_message(message.chat.id, "Please, Enter year again")
                bot.register_next_step_handler(msg, course_year_handler, choice)
            elif int(semester) > 2:
                bot.send_message(message.chat.id, "There are only 2 semesters")
                msg = bot.send_message(
                    message.chat.id, "Please, Enter semester again")
                bot.register_next_step_handler(msg, course_semester_handler, year, choice)
            else:
                course_list = {}
                for i in range(len(courseTitle)):
                    if year1[i].text == year:
                        if sem1[i].text == semester:
                            temp_data = {courseTitle[i].text: credit_hour[i].text}
                            course_list.update(temp_data)

                full_str = "\n".join("{}\t\t{}".format(v, k)
                                    for k, v in course_list.items())
                bot.send_message(message.chat.id, full_str)
    except Exception:
        bot.send_message(message.chat.id,"The database is being updated, please try agian later")