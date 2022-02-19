from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("localhost:27017")

# connect to database
db = client.rant_app

'''
User fields
- email: String
- first_name: String
- last_name: String
- display_name: String
- interests: String[] 
- rants: rant_id[] 
'''

def insert_user(user):
    db.users.insert_one(user)

def get_user(email):
    user = db.users.find_one({"email": email})
    return user

def get_user_field(email, field):
    return db.users.find_one({"email": email},{field: 1, "_id": 0})[field]

def get_users():
    users = db.users.distinct("email")
    return users

def update_user(email, key, value):
    user = db.users.find_one({"email": email})
    if key not in user.keys():
        db.users.update_one({"email": email}, {"$set": {key:value}})
    elif type(user[key]) != list:
        db.users.update_one({"email": email}, {"$set": {key:value}})
    else:
        db.users.update_one({"email": email}, {"$push": {key: value}})

#TODO: update this from /username/my-profile endpoint
def delete_user(email):
    db.users.delete_one({"email": email})
    return False

"""
Rant fields
rant_id: String (email + count)
email: (foreign key): string
text: string
sentiment_score: int
categories: string[] 
"""
def insert_rant(rant):
    db.rants.insert_one(rant)
    update_user(rant["email"], "rants", rant['rant_id'])

def get_rants(email):
    rants = db.rants.find({"email": email})
    return dumps(list(rants))

def match_rant(rant_id):
    user_rant = db.rants.find_one({"rant_id": "rant_id"})
    rant_sentiment = user_rant["sentiment_score"]
    rant_categories = user_rant["categories"]
    matched_rant = db.rants.find_one({"sentiment_score": rant_sentiment, "categories": {"$in": rant_categories}})

    if matched_rant is None:
        return {"No match"}
    return matched_rant

if __name__ == "__main__":
    # insert_user({"username": "ryanmle2001"})
    print(get_users())
    # update_user("ryanmle2001@gmail.com", "interests", ["math"])
    # update_user("ryanmle2001@gmail.com", "interests", "sports")
    # print(get_user_field('ryanmle2001@gmail.com', "age"))
    print(get_rants("ryanmle2001@gmail.com"))

