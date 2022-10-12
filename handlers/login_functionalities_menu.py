from functionalities.SIMS.bdu_sims_login import driver_transfer
from util.useful_lists import *
from util.keyboard_buttons import buttons
from handlers.back_button_handler import still_loggedin_checker
from functionalities.SIMS.MyGrades import My_Grades
from functionalities.SIMS.MyCourses import All_Courses,course_year_handler
from functionalities.SIMS.MyStatus import current_cgpa,status_year_handler,sgrade_year_handler
from bot import bot


def functionalities_menu_messages(message):
    web = driver_transfer()
    if master_check[0] == '1':
        if message.text == success_login[0]: # My Courses page
            bot.send_message(message.from_user.id, success_login[0],
                            reply_markup=buttons("my_courses"))
        elif message.text == success_login[1]: # My Status page
            bot.send_message(message.from_user.id, success_login[1],
                            reply_markup=buttons("my_status"))
        elif message.text == success_login[2]: # My Grades page
            sent_msg = bot.send_message(message.from_user.id, "Getting Grades ... ",
                            reply_markup=buttons("s_login"))
            My_Grades(message,sent_msg,web)
        elif message.text == success_login[3]: # My Dormitory page
            bot.send_message(message.from_user.id, success_login[3],
                            reply_markup=buttons("s_login"))
        elif message.text == MyC[0]: # All Courses
            sent_msg = bot.send_message(message.from_user.id, "Getting all courses . . .",
                            reply_markup=buttons("my_courses"))
            All_Courses(message,sent_msg,web)
        elif message.text == MyC[1]: # Courses given on a specific year
            msg = bot.send_message(message.from_user.id, "Enter year",
                                reply_markup=buttons("my_courses"))
            choice = 'y'
            bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
        elif message.text == MyC[2]: # Courses given on a specific semester
            msg = bot.send_message(message.from_user.id, "Enter year",
                                reply_markup=buttons("my_courses"))
            choice = 's'
            bot.register_next_step_handler(msg, course_year_handler, choice,web,msg)
        elif message.text == MyS[0]: # Cumulative GPA - CGPA
            current_cgpa(message,web)
        elif message.text == MyS[1]: # Semester GPA - SGPA
            msg = bot.send_message(message.from_user.id, "Enter year",
                                reply_markup=buttons("my_status"))
            bot.register_next_step_handler(msg, status_year_handler,web,msg)
        elif message.text == MyS[2]: # Semester Grades
            msg = bot.send_message(message.from_user.id, "Enter year",
                                reply_markup=buttons("my_status"))
            bot.register_next_step_handler(msg, sgrade_year_handler,web,msg)
        elif message.text == "Back":
            bot.send_message(message.from_user.id, "Back",reply_markup=buttons("s_login"))
        elif message.text == "Back to Menu":
            still_loggedin_checker(message,web)
    else:
        bot.send_message(message.from_user.id, "You are not logged in yet, press the login button to login")
