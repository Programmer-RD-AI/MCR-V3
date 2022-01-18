from datetime import datetime

from mongodb.get_the_last_id import *
from server import *


class Stream:
    def __init__(self, message, user_name, role):
        self.message = message
        self.user_name = user_name
        self.role = role
        if self.role == "Admin":
            self.user_name = "Admin"
        self.db = cluster["Stream"]
        self.collection = self.db["Stream"]

    def add(self):
        _id = get_custom_last_id(db="Stream", collection="Stream")
        self.collection.insert_one({
            "_id": _id,
            "Message": self.message,
            "Role": self.role,
            "User Name": self.user_name,
            "time": datetime.now(),
        })
        return True

    def delete(self, _id, user_name):
        results = []
        for result in self.collection.find({"_id": int(_id)}):
            results.append(result)
        if results[0]["Role"] != user_name:
            return False
        self.collection.delete_one(results[0])
        print(results)
        return True

    def get(self):
        results = []
        for result in self.collection.find({}):
            results.append(result)
        return results

    def get_message_with_id(self, _id_of_message):
        results = []
        for result in self.collection.find({"_id": _id_of_message}):
            results.append(result)
        return results
