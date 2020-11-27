from pymongo import *
import json
from mailer import Mailer
import threading


si = Sign_In(user_name="Ranuga-D", password_or_email="go2ranuga@gmail.com", role="Programmer")
result = si.check()
print(result)
