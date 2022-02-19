from pymongo import MongoClient
from pprint import pprint
import json


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

def get_user(username):
    user = db.users.find_one({"username": username})
    return user

# String username
def insert_user(user):
    db.users.insert_one(user)

#String username, dict field
def update_user(username, field):
    user = db.users.find_one({"username": username})
    key = field.key()
    value = field.value()
    user[key] = value

def delete_user():
    return False
# Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)
