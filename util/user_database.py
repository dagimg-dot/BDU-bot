from pymongo import MongoClient
from config import db
from util.initiate_webdriver import initiate_driver


cluster = MongoClient(db)

db = cluster["Telegram"]
collection = db["Users"]

users = {}

class User:
    def __init__(self, user_id, first_name):
        self.user_id = user_id
        self.first_name = first_name
        self.is_logged_in = False
        self.is_driver_opened = False
        self.OpenWeb = {
            "My Courses": False,
            "My Status": False,
            "My Grades": False,
            "Semester Grades": False
        }

    def get_webdriver(self):
        self.driver = initiate_driver()
    
    def get_state(self):
        return self.OpenWeb

    def set_state(self,key,is_open):
        self.OpenWeb[key] = is_open


