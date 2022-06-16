import os
from httplib2 import Response
import requests


class SmsService:
    def __init__(self):
        self.url = os.environ.get("HAHU_SMS_API_ENDPOINT")

    def send_sms(self, phone_number, message) -> bool:
        response: Response = requests.get(
            self.url,
            params={
                "phone": phone_number.replace("+", ""),
                "message": message,
                "device": os.environ.get("HAHU_SMS_API_DEVICE"),
                "key": os.environ.get("HAHU_SMS_API_KEY"),
            },
        )

        response_json: dict = response.json()
        if response_json["status"] == 200:
            return True
        else:
            return False
