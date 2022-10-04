from bot import bot
from telebot import types
import json


with open('util\Courses\Freshman_courses.json') as fresh:
            freshman_data = json.load(fresh)

def get_add_info(message,msg):
    
