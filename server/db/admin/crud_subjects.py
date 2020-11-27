from server import *


subject_db = cluster["Subjects"]


class Subjects:
    def __init__(self, subject):
        self.collection = subject_db[subject]
        self.subject = subject

    def add_collection(self):
        try:
            results = subject_db.collection_names()
            if self.subject in results:
                return False
            self.collection.insert_one({"test": "test"})
            self.collection.delete_many({})
            return True
        except:
            return False

    def delete_collection(self):
        try:
            results = subject_db.collection_names()
            if self.subject in results:
                self.collection.drop()
                return True
            return False
        except:
            return False

    def get_collections(self):
        try:
            results = subject_db.collection_names()
            return results
        except:
            return False

    def update_collection(self, old_name):
        try:
            subject_db[old_name].rename(self.subject)
            return True
        except:
            return False

    def check_if_exits(self):
        results = subject_db.collection_names()
        if self.subject in results:
            return True
        return False