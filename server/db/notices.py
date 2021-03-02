from server import *
from mongodb.get_the_last_id import *
db = cluster["Notices"]
collection = db["Notices"]


def add_notice(title, description):
    collection.insert_one(
        {
            "_id": get_custom_last_id(db="Notices", collection="Notices"),
            "Title": title,
            "Description": description,
        }
    )
    return True


def get_notices():
    try:
        results = []
        for result in collection.find({}):
            results.append(result)
        return results
    except:
        return []


def delete_notice(title, description):
    try:
        collection.delete_one({"Title": title, "Description": description})
        return True
    except:
        return False