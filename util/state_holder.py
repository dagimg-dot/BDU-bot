from util.user_database import users

def user_state_changer(message,state):
    for key in users[message.from_user.id].get_user_state().keys():
        if key == state:
            users[message.from_user.id].set_user_state(key,users[message.from_user.id].get_user_state()[key]+1)
        else:
            users[message.from_user.id].set_user_state(key,0)
    # for i in range(len(dept_title)):
    #     users[message.from_user.id].dept_state.a
    for i in range(5):
        if i == 0:
            users[message.from_user.id].set_rev_state(i,1)
        else:
            users[message.from_user.id].set_rev_state(i,0)
    users[message.from_user.id].gpa_list.clear()
    users[message.from_user.id].possibility_dict.clear()


def user_state_reset(message):
    for key in users[message.from_user.id].get_user_state().keys():
        users[message.from_user.id].set_user_state(key,0)

def rev_state_changer():
    pass

def rev_state_reset(message):
    for i in range(5):
        users[message.from_user.id].set_rev_state(i,0)

def dept_state_changer():
    pass

def dept_state_reset():
    pass