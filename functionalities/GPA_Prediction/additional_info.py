from bot import bot
import json
from functionalities.GPA_Prediction.reverse_prediction import GPA_validator, course_display
from util.interrupter import step_canceler
from util.message_cleaner import cleaner
from util.useful_lists import cardinal_ordinal,dept_title,data,Grades,menu
from functionalities.GPA_Prediction.gpa_calc import gpa_calculator
from util.user_database import users
from os import path
import re


def get_add_info(message,msg):
    if msg == dept_title[0]:
        year = "1" # This is has no purpose
        sent_msgS = bot.send_message(message.from_user.id,"Enter semester")
        bot.register_next_step_handler(sent_msgS,semester_handler,year,sent_msgS,msg)
    elif msg == dept_title[1]:
        with open('util\Courses\Pre-Engineering.json') as pre:
            pre_data = json.load(pre)

        course_title =  []
        credit = []
        for i in range(len(pre_data)):
            course_title.append(pre_data[i]['Course Title'])
            credit.append(pre_data[i]['Credit'])

        intro = "These are the courses for Pre - Engineering \n\n"
        if users[message.from_user.id].get_user_state()[menu[1]] >= 1:
            full_str = '\n'.join([str(i) for i in course_title])
            full = intro +"\n\n" + full_str
            bot.send_message(message.from_user.id,full)

            sent_msg = bot.send_message(message.from_user.id,"Please enter the grades for each course separated by comma or whitespaces")
            bot.register_next_step_handler(sent_msg,grade_validator,course_title,credit)
        elif users[message.from_user.id].get_user_state()[menu[2]] >= 1:
            full_msg = course_display(course_title,credit)
            full = intro +"\n\n" + full_msg
            sent_msg = bot.send_message(message.from_user.id,full)
            # bot.edit_message_text(full,sent_msg.from_user.id,sent_msg.message_id)
            ask_gpa = "Please enter the the range of GPAs to reverse predict individual grades (e.g: 3.5,3.7)"
            sent_msgR = bot.send_message(message.from_user.id,ask_gpa)
            bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
    else:
        sent_msg = bot.send_message(message.from_user.id,"Enter year")
        bot.register_next_step_handler(sent_msg,year_handler,msg,sent_msg)

def year_handler(message,msg,sent_msg):
    if message.text == '/x':
        step_canceler(message)
    else:
        year = message.text
        cleaner(message)
        sent_msgS = "Enter semester"
        bot.edit_message_text(sent_msgS,sent_msg.chat.id,sent_msg.message_id)
        bot.register_next_step_handler(sent_msg,semester_handler,year,sent_msg,msg)
        
def semester_handler(message,year,sent_msg,msg):
    if message.text == '/x':
        step_canceler(message)
    else:
        semester = message.text
        cleaner(message)
        sent_msgC = "Validating . . ."
        bot.edit_message_text(sent_msgC,sent_msg.chat.id,sent_msg.message_id)
        # cleaner(sent_msg)
        year_sem_validator(message,year,semester,sent_msg,msg)

def year_sem_validator(message,year,semester,sent_msg,msg):
    if msg == dept_title[0]:
        if semester.isdigit() == False:
            sent_msgD = "Enter integers only, please enter semester again"
            bot.edit_message_text(sent_msgD,sent_msg.chat.id,sent_msg.message_id)
            bot.register_next_step_handler(sent_msg,semester_handler,year,sent_msg,msg)
        elif int(semester) > 2:
            sent_msgD = "There are only 2 semesters, please enter semester again"
            bot.edit_message_text(sent_msgD,sent_msg.chat.id,sent_msg.message_id)
            bot.register_next_step_handler(sent_msg,semester_handler,year,sent_msg,msg)
        else:
            with open('util\Courses\Freshman.json') as fresh:
                freshman_data = json.load(fresh)

            course_title =  []
            credit = []
            for i in range(len(freshman_data)):
                if freshman_data[i]['Semester'] == int(semester):
                    course_title.append(freshman_data[i]['Course Title'])
                    credit.append(freshman_data[i]['Credit'])

            intro = "These are the courses for Freshman year " + cardinal_ordinal[int(semester)] + " semester"
            if users[message.from_user.id].get_user_state()[menu[1]] >= 1:
                full_str = '\n'.join([str(i) for i in course_title])
                full = intro +"\n\n" + full_str
                bot.edit_message_text(full,sent_msg.chat.id,sent_msg.message_id)

                grade_input(message,course_title,credit)

            elif users[message.from_user.id].get_user_state()[menu[2]] >= 1:
                full_msg = course_display(course_title,credit)
                full = intro +"\n\n" + full_msg
                bot.edit_message_text(full,sent_msg.chat.id,sent_msg.message_id)
                ask_gpa = "Please enter the the range of GPAs to reverse predict individual grades (e.g: 3.5,3.7)"
                sent_msgR = bot.send_message(message.from_user.id,ask_gpa)
                bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)


    else:
        for i in range(2,len(dept_title)):
            if msg == dept_title[i]:
                if year.isdigit() == False or semester.isdigit() == False:
                    sent_msgD = "Enter integers only, please enter year again"
                    bot.edit_message_text(sent_msgD,sent_msg.chat.id,sent_msg.message_id)
                    bot.register_next_step_handler(sent_msg,year_handler,msg,sent_msg)
                elif int(year) > data[i]['Total Year'] and int(semester) > 2:
                    sent_msgYS = data[i]['Department Title'] + " is given in total of " + str(data[i]['Total Year']) + " years, and each year is divided into 2 semesters.\nPlease enter year again"
                    bot.edit_message_text(sent_msgYS,sent_msg.chat.id,sent_msg.message_id)
                    bot.register_next_step_handler(sent_msg,year_handler,msg,sent_msg)
                elif int(year) > data[i]['Total Year']:
                    sent_msgY = data[i]['Department Title'] + " is given in total of " + str(data[i]['Total Year']) + " years.\nPlease enter year again"
                    bot.edit_message_text(sent_msgY,sent_msg.chat.id,sent_msg.message_id)
                    bot.register_next_step_handler(sent_msg,year_handler,msg,sent_msg)
                elif int(semester) > 2:
                    sent_msgD = "There are only 2 semesters, please enter semester again"
                    bot.edit_message_text(sent_msgD,sent_msg.chat.id,sent_msg.message_id)
                    bot.register_next_step_handler(sent_msg,semester_handler,year,sent_msg,msg)     
                else:
                    dept_identifier(message,year,semester,msg,sent_msg)

def dept_identifier(message,year,semester,msg,sent_msg):
    for i in range(2,len(dept_title)):
            if msg == dept_title[i]:
                start_path = 'util\Courses'
                file = dept_title[i] + '.json'
                location = path.join(start_path,file)
                with open(location) as fresh:
                    course_data = json.load(fresh)

                course_title =  []
                credit = []
                for i in range(len(course_data)):
                    if course_data[i]['Year'] == int(year) and course_data[i]['Semester'] == int(semester):
                        course_title.append(course_data[i]['Course Title'])
                        credit.append(course_data[i]['Credit'])
                
                empty_list = "There are no courses given in " + cardinal_ordinal[int(year)]+" year " + cardinal_ordinal[int(semester)] + " semester"
                if len(course_title) == 0:
                    bot.edit_message_text(empty_list,sent_msg.chat.id,sent_msg.message_id)
                else:
                    intro = "These are the courses for "+ cardinal_ordinal[int(year)]+" year " + cardinal_ordinal[int(semester)] + " semester"
                    if users[message.from_user.id].get_user_state()[menu[1]] >= 1:
                        full_str = '\n'.join([str(i) for i in course_title])
                        full = intro +"\n\n" + full_str
                        bot.edit_message_text(full,sent_msg.chat.id,sent_msg.message_id)

                        grade_input(message,course_title,credit)     
                    elif users[message.from_user.id].get_user_state()[menu[2]] >= 1:
                        full_msg = course_display(course_title,credit)
                        full = intro +"\n\n" + full_msg
                        bot.edit_message_text(full,sent_msg.chat.id,sent_msg.message_id)
                        ask_gpa = "Please enter the the range of GPAs to reverse predict individual grades (e.g: 3.5,3.7)"
                        sent_msgR = bot.send_message(message.from_user.id,ask_gpa)
                        bot.register_next_step_handler(sent_msgR,GPA_validator,course_title,credit,sent_msgR)
                             


def grade_input(message,course_title,credit):
    sent_msgG = bot.send_message(message.from_user.id,"Please enter the grades for each course separated by comma or whitespaces")
    bot.register_next_step_handler(sent_msgG,grade_validator,course_title,credit)

def grade_validator(message,course_title,credit):
    if message.text == '/x':
        step_canceler(message)
    else:
        sent_msgC = "Validating . . ."
        sent_msg = bot.send_message(message.from_user.id,sent_msgC)
        predicted_grades= message.text
        # cleaner(message)
        splitted_grades_uf = re.split(r'[,\s]',predicted_grades)
        splitted_grades = list(filter(None,splitted_grades_uf))

        check_invalid_grade = all(i in Grades for i in splitted_grades)

        if check_invalid_grade == False:
            sent_msgI = "An invalid grade is found from the grades you entered. Please enter them again"
            bot.edit_message_text(sent_msgI,sent_msg.chat.id,sent_msg.message_id)
            bot.register_next_step_handler(sent_msg,grade_validator,course_title,credit)
        elif len(splitted_grades) != len(course_title):
            sent_msgN = "The grades you entered must be equal to the courses in the given semester. Please enter them again"
            bot.edit_message_text(sent_msgN,sent_msg.chat.id,sent_msg.message_id)
            bot.register_next_step_handler(sent_msg,grade_validator,course_title,credit)
        else:
            splitted_upper = []
            for i in range(len(splitted_grades)):
                splitted_upper.append(splitted_grades[i].upper())

            course_grade = {}
            for i in range(len(course_title)):
                temp_data = {course_title[i]: splitted_upper[i]}
                course_grade.update(temp_data)

            full_str = "\n".join("{0}  {1}".format(v, k)
                                for k, v in course_grade.items())
            bot.edit_message_text(full_str,sent_msg.chat.id,sent_msg.message_id)
            gpa_calculator(message,credit,splitted_upper)
    
