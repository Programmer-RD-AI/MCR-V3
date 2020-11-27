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

    @staticmethod
    def get_data_of_teacher(user_name, email):
        try:
            results = []
            for result in auth_collection_sign_in.find(
                {"User Name": user_name, "Email": email}
            ):
                results.append(result)
            if result == []:
                return [False, result]
            return [True, result]
        except:
            return False

    def update_teacher(self, new_info: dict, old_info: dict):
        try:
            results = []
            if new_info["Role"] is "Student":
                new = {
                    "$set": {
                        "User Name": new_info["User Name"],
                        "Password": new_info["Password"],
                        "Email": new_info["Email"],
                        "Role": new_info["Role"],
                    }
                }
                self.subject_collection.delete_one(old_info)
            else:
                new = {
                    "$set": {
                        "User Name": new_info["User Name"],
                        "Password": new_info["Password"],
                        "Email": new_info["Email"],
                        "Role": new_info["Role"],
                        "Subject": new_info["Subject"],
                    }
                }
            auth_collection_sign_in.update_one(old_info, new)
            return True
        except:
            return False

    @staticmethod
    def get_teachers(subject):
        subject_collection = subject_db[subject]
        results_subjects = []
        for result_subjects in subject_collection.find({}):
            results_subjects.append(result_subjects)
        results_user = []
        for result_user in auth_collection_sign_in.find({"Role": "Teacher"}):
            results_user.append(result_user)
        return [results_user, results_subjects]


class Students:
    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = password
        self.email = email

    def __repr__(self):
        return "Teacher"

    def add_student(self):
        try:
            si1 = Sign_In(
                user_name=self.user_name,
                password_or_email=self.password,
                role="Student",
            )
            si2 = Sign_In(
                user_name=self.user_name, password_or_email=self.email, role="Student"
            )
            results = [si1.check(), si2.check()]
            if results[0][0] is False and results[1][0] is False:
                return [False, "There is another student with the same info ! "]
            auth_collection_sign_in.insert_one(
                {
                    "User Name": self.user_name,
                    "Password": self.password,
                    "Email": self.email,
                    "Role": "Student",
                }
            )
            return [True, "New Student Created ! "]
        except:
            return [False, "An Error Occurred ! "]

    def delete_student(self):
        pass

    def update_student(self):
        pass

    def get_students(self):
        pass