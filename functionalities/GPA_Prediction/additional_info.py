from tkinter import SEPARATOR
from tkinter.ttk import Separator
from numpy import full
from requests import get
from bot import bot
from telebot import types
import json
from util.useful_lists import cardinal_ordinal,dept_title,data
from os import path
import re


def get_add_info(message,msg):
    if msg == dept_title[0]:
        year = "1"
        sent_msg = bot.send_message(message.chat.id,"Enter semester")
        bot.register_next_step_handler(sent_msg,semester_handler,year,msg)
    elif msg == dept_title[1]:
        with open('util\Courses\Pre-Engineering.json') as pre:
            pre_data = json.load(pre)

        course_title =  []
        for i in range(len(pre_data)):
            course_title.append(pre_data[i]['Course Title'])

        full_str = '\n'.join([str(i) for i in course_title])
        bot.send_message(message.chat.id,"These are the courses for Pre - Engineering \n\n" + full_str)

        sent_msg = bot.send_message(message.chat.id,"Please enter the grades for each course separated by comma or whitespaces")
        bot.register_next_step_handler(sent_msg,grade_validator,msg)
    else:
        sent_msg = bot.send_message(message.chat.id,"Enter year")
        bot.register_next_step_handler(sent_msg,year_handler,msg)

def year_handler(message,msg):
    year = message.text
    sent_msg = bot.send_message(message.chat.id,"Enter semester")
    bot.register_next_step_handler(sent_msg,semester_handler,year,msg)

def semester_handler(message,year,msg):
    semester = message.text
    year_sem_validator(message,year,semester,msg)

def year_sem_validator(message,year,semester,msg):
    if msg == dept_title[0]:
        if int(semester) > 2:
            bot.send_message(message.chat.id,"There are only 2 semesters.")
            year_handler(message,msg)
        else:
            with open('util\Courses\Freshman.json') as fresh:
                freshman_data = json.load(fresh)
            course_title =  []
            for i in range(len(freshman_data)):
                if freshman_data[i]['Semester'] == int(semester):
                    course_title.append(freshman_data[i]['Course Title'])

            full_str = '\n'.join([str(i) for i in course_title])
            bot.send_message(message.chat.id,"These are the courses for Freshman year " + cardinal_ordinal[int(semester)] + " semester\n\n" + full_str)

            sent_msg = bot.send_message(message.chat.id,"Please enter the grades for each course separated by comma or whitespaces")
            bot.register_next_step_handler(sent_msg,grade_validator,msg)
    else:
        for i in range(2,len(dept_title)):
            if msg == dept_title[i]:
                if int(year) > data[i]['Total Year'] and int(semester) > 2:
                    sent_msg = data[i]['Department Title'] + " is given in total of " + str(data[i]['Total Year']) + " years, and each year is divided into 2 semesters."
                    bot.send_message(message.chat.id,sent_msg)
                    get_add_info(message,msg)
                elif int(year) > data[i]['Total Year']:
                    sent_msg = data[i]['Department Title'] + " is given in total of " + str(data[i]['Total Year']) + " years."
                    bot.send_message(message.chat.id,sent_msg)
                    get_add_info(message,msg)
                elif int(semester) > 2:
                    bot.send_message(message.chat.id,"There are only 2 semesters.")
                    year_handler(message,msg)
                else:
                    dept_identifier(message,year,semester,msg)

def dept_identifier(message,year,semester,msg):
    for i in range(2,len(dept_title)):
            if msg == dept_title[i]:
                start_path = 'util\Courses'
                file = dept_title[i] + '.json'
                location = path.join(start_path,file)
                with open(location) as fresh:
                    course_data = json.load(fresh)

                course_title =  []
                for i in range(len(course_data)):
                    if course_data[i]['Year'] == int(year) and course_data[i]['Semester'] == int(semester):
                        course_title.append(course_data[i]['Course Title'])
                
                full_str = '\n'.join([str(i) for i in course_title])
                bot.send_message(message.chat.id,"These are the courses for "+ cardinal_ordinal[int(year)]+" year " + cardinal_ordinal[int(semester)] + " semester\n\n" + full_str)
                sent_msg = bot.send_message(message.chat.id,"Please enter the grades for each course separated by comma or whitespaces")
                bot.register_next_step_handler(sent_msg,grade_validator,msg)

def grade_validator(message,msg):
    predicted_grades= message.text
    splitted_grades = re.split(r'[,\s]',predicted_grades)
    for i in splitted_grades:
        for i in splitted_grades:
            if i == '':
                splitted_grades.remove(i)
    full_str = '\n'.join([str(i) for i in splitted_grades])
    bot.send_message(message.chat.id,full_str)
 
