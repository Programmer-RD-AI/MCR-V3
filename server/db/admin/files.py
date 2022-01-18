import base64
import os
import random
import shutil

import bson
from bson.binary import Binary

from mongodb.get_the_last_id import *
from server import *


class File_Admin:
    def __init__(self, file, description):
        self.file = file
        self.file_2 = file
        self.db = cluster["File"]
        self.description = description

    def add(self, file, file_type_name):
        collection = self.db[str(file_type_name)]
        choice = random.randint(0, 1000000000000)
        if file.filename in os.listdir(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/"
        ):
            file.filename = f"{choice}{file.filename}"
        file.save(
            os.path.join(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/",
                file.filename,
            ))

        with open(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/{file.filename}",
                "rb",
        ) as f:
            encoded = Binary(f.read())
        _id = get_custom_last_id(db="File", collection=file_type_name)
        results = []
        for result in collection.find({"_id": _id}):
            results.append(result)
        if results != []:
            _id = _id + 2
            results = []
            for result in collection.find({"_id": _id}):
                results.append(result)
            if results != []:
                _id = _id + 1
        collection.insert_one({
            "_id": _id,
            "file": encoded,
            "filename": self.file_2.filename,
            "desc": self.description,
            "file_type_name": file_type_name,
        })
        os.remove(
            f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/{self.file.filename}"
        )
        return True

    def get_all_files(self, file_type_name):
        results = []
        collection = self.db[file_type_name]
        for result in collection.find():
            results.append(result["filename"])
        print(results)
        return results

    def get(self, description, filename, file_type_name):
        results = []
        collection = self.db[str(file_type_name)]
        choice = random.randint(0, 100000000)
        for result in collection.find({
                "filename": filename,
                "desc": description,
                # "file_type_name": file_type_name,
        }):
            results.append(result)
        print("*" * 100)
        print(results)
        print("+" * 100)
        # file = open(f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/file/{file_type_name}/{results[0]['filename']}",
        # "w",
        # )
        # file.write("")
        # file.close()
        if file_type_name not in os.listdir(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/file/"
        ):
            os.mkdir(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/file/{file_type_name}/"
            )
        # except:
        #     os.mkdir(
        #         f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/file/{file_type_name}"
        #     )
        try:
            with open(
                    f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/file/{file_type_name}/{results[0]['filename']}",
                    "wb",
            ) as file:
                file.write(results[0]["file"])
        except:
            pass
        return [
            f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/file/{file_type_name}/",
            results[0]["filename"],
        ]

    def delete(self, description, filename, file_type_name):
        collection = self.db[str(file_type_name)]
        collection.delete_one({
            "desc": description,
            "filename": filename,
            "file_type_name": file_type_name,
        })
        return True

    def add_file_type(self, file_type_name):
        collection = self.db[file_type_name]
        collection.insert_one({})
        collection.delete_one({})
        os.mkdir(
            f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/"
        )
        return True

    def delete_file_type(self, file_type_name):
        collection = self.db[file_type_name]
        collection.drop()
        try:
            print("Done 1")
            os.remove(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/"
            )
            print("Done 1")
        except:
            shutil.rmtree(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}"
            )
        else:
            shutil.rmtree(
                f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{file_type_name}/"
            )
        print("Done")
        return True

    def get_all_file_types(self):
        collection_names = self.db.list_collection_names()
        return collection_names

    def update_file_type(self, old_file_name, new_file_name):
        if old_file_name == new_file_name:
            return [False]
        old_collection = self.db[old_file_name]
        results = []
        for result in old_collection.find():
            result["file_type_name"] = new_file_name
            results.append(result)
        old_collection.drop()
        os.rename(
            f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{old_file_name}/",
            f"/home/ranuga/Programming/Projects/Python/Flask/Done/My-Class-Room-V2/files/{new_file_name}/",
        )
        new_file_name = self.db[new_file_name]
        if results == []:
            results.append({"_id": 0})
        new_file_name.insert_many(results)
        new_file_name.delete_one({"_id": 0})
        return [True]

    def get_all_files_in_a_file_type(self, file_type_name):
        collection = self.db[file_type_name]
        results = []
        for result in collection.find():
            results.append(result)
        return results
