from server import *
import requests
from mongodb.get_the_last_id import *


class SMS:
    def __init__(self, phone_numbers, message):
        self.phone_numbers = phone_numbers
        self.message = message
        self.url = "http://sender.marxhal.com/api/v2/send.php"
        self.user_id = "102076"
        self.api_key = "sgpi7msoyxkq2qhnn"
        self.sender_id = "VOTE 21"
        self.db = cluster["SMS"]
        self.collection = self.db["SMS"]
        self.last_id = get_custom_last_id(db="SMS", collection="SMS")

    def send(self):
        old_balance = float(self.get_balance())
        for phone_number in self.phone_numbers:
            print(phone_number)
            result = requests.post(
                self.url,
                {
                    "user_id": self.user_id,
                    "api_key": self.api_key,
                    "sender_id": self.sender_id,
                    "to": "+" + str(phone_number),
                    "message": self.message,
                },
            )
            print(result.json())
        new_balance = float(self.get_balance())
        self.add_logs()
        return [True, old_balance - new_balance]

    def add_logs(self):
        self.collection.insert_one(
            {
                "_id": self.last_id,
                "Phone Numbers": self.phone_numbers,
                "Message": self.message,
            }
        )
        return True

    def get_logs(self):
        results = []
        for result in self.collection.find():
            results.append(result)
        return results

    def get_balance(self):
        url = "http://sender.marxhal.com/api/v2/status.php"
        balance = requests.post(url, {"user_id": self.user_id, "api_key": self.api_key})
        return balance.json()["result"]["account_balance"]

    def add_balance(self, amount):
        # +94718024596 is the phone number of the person who updates the price.
        sms = SMS(
            phone_numbers=["+94718024596"],
            message=f"Can you pls add {amount} to my account pls.",
        )
        sms.send()
        return True
