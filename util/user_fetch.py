from util.user_database import collection, users, User

# fetches existing users from the database whenever the bot restarts
def fetchUsers():
    try:
        all_users = list(collection.find())
        for i in range(len(all_users)):
            to_dict = {all_users[i]['_id']: User(all_users[i]['_id'],all_users[i]['f_name'])}
            users.update(to_dict)
        print("Users fetched successfully")
    except:
        print("An error has occured")
        