from server import *
from server.db.home.autentication import auth_collection_sign_in

subject_db = cluster["Subjects"]


class Subjects:

    def __init__(self, subject):
        try:
            self.collection = subject_db[subject]
            self.subject = subject
        except:
            self.collection = subject
            self.subject = subject

    def add_collection(self):
        try:
            results = subject_db.collection_names()
            if self.collection == self.subject is True or self.subject in results:
                return False
            self.collection.insert_one({"Subject": self.subject})
            self.collection.delete_many({})
            return True
        except:
            return False

    def delete_collection(self):
        try:
            results = subject_db.collection_names()
            if self.subject in results:
                self.collection.drop()
                results_ = []
                for result_ in auth_collection_sign_in.find({
                        "Subject": self.subject,
                        "Role": "Teacher"
                }):
                    results_.append(result_)
                for result_delete in results_:
                    auth_collection_sign_in.delete_one(result_delete)
                return True
            return False
        except:
            return False

    @staticmethod
    def get_collections():
        try:
            results = subject_db.collection_names()
            string_results = " "
            for result in results:
                string_results = string_results + " " + result + " "
            words = string_results.split()
            words.sort()
            final_result = []
            for word in words:
                final_result.append(word)
            return final_result
        except:
            return False

    def update_collection(self, old_name):
        subject_db[old_name].rename(self.subject)
        results = []
        for result in auth_collection_sign_in.find({
                "Subject": old_name,
                "Role": "Teacher"
        }):
            results.append(result)
        for result_ in results:
            new_values = {"$set": {"Subject": self.subject}}
            auth_collection_sign_in.update_one(result_, new_values)
        return True

    def check_if_exits(self):
        try:
            results = subject_db.collection_names()
            if self.subject in results:
                return True
            return False
        except:
            return False
