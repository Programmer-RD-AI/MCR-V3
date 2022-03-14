import json

from pymongo import *


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


def last_id():
    ids = []
    for _id in collection.find({}):
        ids.append(_id["_id"])
    if ids == []:
        ids = 0
    else:
        ids = ids[-1] + 1
    return ids


def get_custom_last_id(db, collection):
    try:
        db_ = cluster[db]
        collection_ = db_[collection]
        ids = []
        for _id in collection_.find({}):
            ids.append(_id["_id"])
        if ids == []:
            ids = 0
        else:
            ids = ids[-1] + 1
        return ids
    except:
        return 0
