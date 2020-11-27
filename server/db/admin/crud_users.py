from server import *
from server.db.home.autentication import *

user_db = cluster["Auth"]
auth_collection_sign_in = user_db["Auth-Sign-In"]

subject_db = cluster["Subjects"]


class Teacher:
    def __init__(self, user_name, password, email, subject):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.subject = subject
        self.subject_collection = subject_db[subject]

    def __repr__(self):
        return "Teacher"

    def add_teacher(self):
        si1 = Sign_In(
            user_name=self.user_name, password_or_email=self.password, role="Teacher"
        )
        si2 = Sign_In(
            user_name=self.user_name, password_or_email=self.email, role="Teacher"
        )
        results = [si1.check(), si2.check()]
        if results[0][0] is False and results[1][0] is False:
            return [False, "There is another teacher with the same info ! "]
        auth_collection_sign_in.insert_one(
            {
                "User Name": self.user_name,
                "Password": self.password,
                "Email": self.email,
                "Role": "Teacher",
                "Subject": self.subject,
            }
        )
        self.subject_collection.insert_one(
            {
                "User Name": self.user_name,
                "Password": self.password,
                "Email": self.email,
                "Role": "Teacher",
                "Subject": self.subject,
            }
        )
        return [True, "New Teacher Created ! "]

    def delete_teacher(self, email, user_name):
        try:
            results = []
            for result in auth_collection_sign_in.find_one(
                {"User Name": user_name, "Email": email}
            ):
                results.append(result)
            if results == []:
                return False
            for result_ in results:
                try:
                    auth_collection_sign_in.delete_one(result_)
                except:
                    pass
            return True
        except:
            return False

    def update_teacher(self, new_info: list, user_name: str, email: str):
        try:
            results = []
            
        except:
            return False

    @staticmethod
    def get_teachers(subject):
        subject_collection = subject_db[subject]
        results_subjects = []
        for result_subjects in subject_collection.find({}):
            results_subjects.append(result_subjects)
        results_user = []
        for result_user in results_user.find({}):
            results_user.append(result_user)
        return [results_user, results_subjects]


class Students:
    def __init__(self):
        pass

    def __repr__(self):
        return "Teacher"

    def add_student(self):
        pass

    def delete_student(self):
        pass

    def update_student(self):
        pass

    def get_students(self):
        pass