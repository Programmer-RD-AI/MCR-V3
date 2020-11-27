import json
from pymongo import *


def get_link():
    with open(
        "/home/ranuga/Programming/Projects/Python/Flask/Doing/My-Class-Room-V2/private/mongodb-client.json"
    ) as json_info:
        info = json.load(json_info)
    return info["MongoDB-Client-Url"]


link = get_link()
cluster = MongoClient(link)
db = cluster["Auth"]
collection = db["Auth-Sign-In"]
user_name = input("User Name : ")
password = input("Password")
email = input("Email : ")
collection.insert_one(
    {"User Name": user_name, "Password": password, "Email": email, "Role": "Admin"}
)
print("Done...")
