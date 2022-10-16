# from util.useful_lists import OpenWeb
from util.user_database import users

def state_changer(message,page):
    for key,value in users[message.from_user.id].get_state().items():
        if key == page:
            users[message.from_user.id].set_state(key,True)
        else:
            users[message.from_user.id].set_state(key,False)


def state_reset(message):
    for key,value in users[message.from_user.id].get_state().items():
        users[message.from_user.id].set_state(key,False)
