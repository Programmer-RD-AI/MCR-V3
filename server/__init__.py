from flask import *
from flask_restful import *
from pymongo import *
import json
from firebase import firebase


def get_link():
    with open(
        "/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/private/mongodb-client.json"
    ) as json_info:
        info = json.load(json_info)
    return info["MongoDB-Client-Url"]


# Configing the web application
app = Flask(__name__)
app.debug = True
app.secret_key = "--568963558fgdg85fbfd/8gf6bed8fgf6dbhde9rfg5sdf96eyhgr96f5hr9ehr--Ranuga D 2008--568963558fgdg85fbfd/8gf6bed8fgf6dbhde9rfg5sdf96eyhgr96f5hr9ehr--"
api = Api(app)
# COnfiging the databases
firebase = firebase.FirebaseApplication(
    "https://my-class-room-v2.firebaseio.com/", None
)
link = get_link()
cluster = MongoClient(link)
from server.routes import *
