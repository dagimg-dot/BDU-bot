from util.message_cleaner import cleaner
from util.state_holder import state_changer
from util.useful_lists import *
from util.keyboard_buttons import buttons
from handlers.back_button_handler import still_loggedin_checker
from functionalities.SIMS.MyGrades import My_Grades
from functionalities.SIMS.MyCourses import All_Courses,course_year_handler
from functionalities.SIMS.MyStatus import current_cgpa,sgpa_year_handler,sgrade_year_handler
from bot import bot
from util.user_database import users

def functionalities_menu_messages(message):
    if users[message.from_user.id].is_logged_in == True:
        if message.text == success_login[0]: # My Courses page
            bot.send_message(message.from_user.id, success_login[0],
                            reply_markup=buttons("my_courses"))
        elif message.text == success_login[1]: # My Status page
            bot.send_message(message.from_user.id, success_login[1],
                            reply_markup=buttons("my_status"))
        elif message.text == success_login[2]: # My Grades page
            sent_msg = bot.send_message(message.from_user.id, "Getting Grades ... ",
                            reply_markup=buttons("s_login"))
            state_changer(message,success_login[2])
            My_Grades(message,sent_msg)
        elif message.text == success_login[3]: # My Dormitory page
            bot.send_message(message.from_user.id, success_login[3],
                            reply_markup=buttons("s_login"))
        elif message.text == MyC[0]: # All Courses
            sent_msg = bot.send_message(message.from_user.id, "Getting all courses . . .",
                            reply_markup=buttons("my_courses"))
            state_changer(message,success_login[0])
            All_Courses(message,sent_msg)
        elif message.text == MyC[1]: # Courses given on a specific year
            msg = bot.send_message(message.from_user.id, "Enter year")
            state_changer(message,success_login[0])
            choice = 'y'
            bot.register_next_step_handler(msg, course_year_handler, choice,msg)
        elif message.text == MyC[2]: # Courses given on a specific semester
            msg = bot.send_message(message.from_user.id, "Enter year")
            state_changer(message,success_login[0])
            choice = 's'
            bot.register_next_step_handler(msg, course_year_handler, choice,msg)
        elif message.text == MyS[0]: # Cumulative GPA - CGPA
            state_changer(message,success_login[1])
            current_cgpa(message)
        elif message.text == MyS[1]: # Semester GPA - SGPA
            msg = bot.send_message(message.from_user.id, "Enter year")
            state_changer(message,success_login[1])
            bot.register_next_step_handler(msg, sgpa_year_handler,msg)
        elif message.text == MyS[2]: # Semester Grades
            # msg = bot.send_message(message.from_user.id, "Enter year")
            bot.send_message(message.from_user.id, "Under Development")
            # state_changer(message,MyS[2])
            # bot.register_next_step_handler(msg, sgrade_year_handler,msg)
        elif message.text == "Back":
            bot.send_message(message.from_user.id, "Back",reply_markup=buttons("s_login"))
            cleaner(message)
        elif message.text == "Back to Menu (Log Out)":
            still_loggedin_checker(message)
    else:
        bot.send_message(message.from_user.id, "You are not logged in yet, press the login button to login")
