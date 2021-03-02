from server import *
from mailer import Mailer
import threading
from mongodb.get_the_last_id import get_custom_last_id

auth_db = cluster["Auth"]
auth_collection_sign_in = auth_db["Auth-Sign-In"]


class Sign_In:
    def __init__(self, user_name, password_or_email, role) -> None:
        self.user_name = user_name
        self.password_or_email = password_or_email
        self.role = role

    def check_user_name_and_password(self):
        results = []
        for result in auth_collection_sign_in.find(
            {
                "User Name": self.user_name,
                "Password": self.password_or_email,
                "Role": self.role,
            }
        ):
            results.append(result)
        if results == []:
            return False
        return True

    def check_user_name_and_email(self):
        results = []
        for result in auth_collection_sign_in.find(
            {
                "User Name": self.user_name,
                "Email": self.password_or_email,
                "Role": self.role,
            }
        ):
            results.append(result)
        print(f"\n \n User Name and Email Results : {results} \n \n ")
        if results == []:
            return False
        return True

    def check(self):
        results = [
            self.check_user_name_and_email(),
            self.check_user_name_and_password(),
        ]
        if results[0] is False and results[1] is False:
            return [False, results]
        else:
            return [True, results]

    def __repr__(self):
        return " - ! Sign In ! - "


class Register:
    def __init__(self, user_name, password, whatsapp_number, email):
        self.user_name = user_name
        self.password = password
        self.whatsapp_number = whatsapp_number
        self.email = email
        self.auth_collection_register = auth_db["Register"]

    def check_if_it_exists(self):
        results_all = []
        for result in auth_collection_sign_in.find(
            {
                "User Name": self.user_name,
                "Password": self.password,
                "Whatsapp Number": self.whatsapp_number,
                "Email": self.email,
            }
        ):
            results_all.append(result)
        results_email_and_user_name = []
        for result in auth_collection_sign_in.find(
            {"User Name": self.user_name, "Email": self.email}
        ):
            results_email_and_user_name.append(result)
        results_password_and_user_name = []
        for result in auth_collection_sign_in.find(
            {"User Name": self.user_name, "Password": self.password}
        ):
            results_password_and_user_name.append(result)
        if (
            results_all == []
            and results_email_and_user_name == []
            and results_password_and_user_name == []
        ):
            return True
        return False

    def check(self):
        results = [self.check_if_it_exists()]
        if False not in results:
            _id = get_custom_last_id(db="Auth", collection="Register")
            self.auth_collection_register.insert_one(
                {
                    "_id": _id,
                    "User Name": self.user_name,
                    "Password": self.password,
                    "Whatsapp Number": self.whatsapp_number,
                    "Email": self.email,
                }
            )
            return [
                True,
                [
                    "Registration Created successfuly you will get a message and a email when you get admited from the teacher of the classroom"
                ],
            ]
        else:
            problems = []
            if results[0] is False:
                problems.append(
                    "There is another user with the information that you enterd please check again."
                )
            return [False, problems]

    def get_all_to_register_users(self):
        results = []
        for result in self.auth_collection_register.find():
            results.append(result)
        return results

    def delete_user(self, _id):
        results = []
        for result in self.auth_collection_register.find({"_id": _id}):
            results.append(result)
        print("+" * 100)
        print(results)
        print("+" * 100)
        if results != []:
            print("YES !!!")
            self.auth_collection_register.delete_one(results[0])
            return [True, results]
        else:
            return [False, []]

    def get_user_info_from__id(self, _id):
        results = []
        for result in self.auth_collection_register.find({"_id": _id}):
            results.append(result)
        if results != []:
            print("YES !!!")
            return [True, results]
        else:
            return [False, []]