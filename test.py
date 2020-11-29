from pymongo import *
import json


def get_link():
    with open(
        "/home/ranuga/Programming/Projects/Python/Flask/Doing/My-Class-Room-V2/private/mongodb-client.json"
    ) as json_info:
        info = json.load(json_info)
    return info["MongoDB-Client-Url"]


# COnfiging the databases
link = get_link()
cluster = MongoClient(link)
auth_db = cluster["Auth"]
auth_collection_sign_in = auth_db["Auth-Sign-In"]
results = []
for result in auth_collection_sign_in.find({'User Name':'RanugaD'}):
    results.append(result)
print(results)