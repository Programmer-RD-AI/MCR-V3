from pymongo import *

cluster = MongoClient(
    "mongodb+srv://Ranuga:Ranuga2008@cluster0.s7lud.mongodb.net/<dbname>?retryWrites=true&w=majority"
)
db = cluster["DB"]
c = ["i", "yu"]
for i in c:
    collection = db['']
    collection.insert_one({"": ""})
    collection.delete_many({})
results = db.collection_names()
print(results)
collection.drop()
results = db.collection_names()
print(results)

results = db.collection_names()
print(results)
