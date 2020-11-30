import json
from pymongo import *
from get_the_last_id import *


def get_link():
    with open(
        "/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/private/mongodb-client.json"
    ) as json_info:
        info = json.load(json_info)
    return info["MongoDB-Client-Url"]


link = get_link()
cluster = MongoClient(link)
db = cluster["Auth"]
collection = db["Auth-Sign-In"]
user_name = input("User Name : ")
password = input("Password : ")
email = input("Email : ")
role = input("Role : ")
teacher = input("T ? (Y/N)")
if teacher.upper() == "Y":
    subject = input("Subject : ")
    for i in range(251):
        id_ = last_id()
        collection.insert_one(
            {
                "_id": id_,
                "User Name": user_name,
                "Password": password,
                "Email": email,
                "Role": role,
                "Subject": subject,
            }
        )
        print(i)
        print("Done...")
else:
    id_ = last_id()
    collection.insert_one(
        {
            "_id": id_,
            "User Name": user_name,
            "Password": password,
            "Email": email,
            "Role": role,
        }
    )
    print("Done...")
