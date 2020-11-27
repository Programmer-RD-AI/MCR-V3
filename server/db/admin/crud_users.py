from server import *


auth_db = cluster["Auth"]
auth_collection_sign_in = auth_db["Auth-Sign-In"]


class User:
    def __init__(self):
        pass

    def __repr__(self):
        return "User"


class Teacher(User):
    def __init__(self):
        pass

    def __repr__(self):
        return "Teacher"

    def add_teacher(self):
        pass

    def delete_teacher(self):
        pass

    def update_teacher(self):
        pass

    def get_teachers(self):
        pass


class Students(User):
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