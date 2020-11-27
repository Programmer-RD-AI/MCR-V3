from server import *
from mailer import Mailer
import threading


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
        print(f"\n \n User Name and Password Results : {results} \n \n ")
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

    def send_email(self, subject, message):
        try:
            mail = Mailer(email="go2ranuga@gmail.com", password="ranuga d 2008")
            mail.send(receiver=self.email, subject=subject, message=message)
            return True
        except:
            return False

    def check(self):
        results = [
            self.check_user_name_and_email(),
            self.check_user_name_and_password(),
        ]
        if results[0] is True or results[1] is True:
            self.send_email("Wrong............", "fdsfsdfd")
            return [True,results]
        else:
            return False

    def __repr__(self):
        return " - ! Sign In ! - "
