from pymongo import MongoClient
from config import db
from util.initiate_webdriver import initiate_driver
from util.useful_lists import success_login,menu,MyS,dept_state_holder

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
        self.user_state = {
            success_login[0]: 0,
            success_login[1]: 0,
            success_login[2]: 0,
            MyS[2]: 0,
            menu[1]: 0,
            menu[2]: 0
        }
        self.dept_state = dept_state_holder
        # self.dept_state = [0,0,0,0,0]
        self.rev_state = [1,0,0,0,0]
        self.possibility_dict = {}
        self.gpa_list = []
        self.current_state = 0
        self.rev_message_id = 0

    def get_webdriver(self):
        self.driver = initiate_driver()
    
    def get_user_state(self):
        return self.user_state

    def set_user_state(self,key,is_open):
        self.user_state[key] = is_open

    def get_rev_state(self,index):
        return self.rev_state[index]
    
    def get_rev_state_full(self):
        return self.rev_state

    def set_rev_state(self,index,state):
        self.rev_state[index] = state

    def get_dept_state(self):
        return self.dept_state

    def set_dept_state(self,index,state):
        self.dept_state[index] = state

