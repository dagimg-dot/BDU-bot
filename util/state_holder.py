from util.user_database import users

def state_changer(message,page):
    for key,value in users[message.from_user.id].get_state().items():
        if key == page:
            users[message.from_user.id].set_state(key,users[message.from_user.id].get_state()[key]+1)
        else:
            users[message.from_user.id].set_state(key,0)


def state_reset(message):
    for key,value in users[message.from_user.id].get_state().items():
        users[message.from_user.id].set_state(key,0)
