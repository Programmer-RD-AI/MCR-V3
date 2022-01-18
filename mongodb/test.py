import base64

import bson
from bson.binary import Binary
from pymongo import *

cluster = MongoClient(
    "mongodb+srv://Ranuga:Ranuga2008@cluster0.xgqas.mongodb.net/<dbname>?retryWrites=true&w=majority"
)
db = cluster["test"]
collectin = db["test"]
with open(
        f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/mongodb/get_the_last_id.py",
        "rb",
) as f:
    encoded = Binary(f.read())
collectin.insert_one({"test": encoded, "file": "get_the_last_id.py"})
results = []
for result in collectin.find({"file": "get_the_last_id.py"}):
    results.append(result)
with open("test.py", "wb") as a:
    a.write(results[0]["test"])
