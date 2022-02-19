from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("localhost:27017")

# connect to database
mongodb = client.rant_app

'''
User fields
- username (primary key): String
- password ? 
- First name: String
- Last name: String
- Display name: String
- Interest: String[] 
- Rants: rant_id[] 
'''
# String username
def insert_user(user):
    mongodb.users.insert_one(user)

def get_user(username):
    user = mongodb.users.find_one({"username": username})
    return user

def get_users():
    users = mongodb.users.distinct("username")
    return users

def get_emails():
    emails = mongodb.users.distinct("email")
    return emails
#String username, dict field
def update_user(username, field):
    user = mongodb.users.find_one({"username": username})
    key = field.key()
    value = field.value()
    user[key] = value

def delete_user():
    return False
# Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)


if __name__ == "__main__":
    # insert_user({"username": "ryanmle2001"})
    print(get_users())