import time
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


class GetimgReger:
    DEFAULT_PASSWORD = "qwe123QWE!@#"
    
    HEADERS = {"X-Requested-With": "XMLHttpRequest"}
    SIGNUP_URL = "https://api.getimg.ai/dashboard/me"
    NEW_KEY_URL = "https://api.getimg.ai/dashboard/keys"
    MESSAGE_URL = "https://www.disposablemail.com/email/id/2"
    MESSAGES_URL = "https://www.disposablemail.com/index/refresh"
    NEW_EMAIL_URL = "https://www.disposablemail.com/index/index"
    
    def __init__(self, *, password: Optional[str] = None) -> None:
        self.session = requests.Session()
        self.password = password if password else self.DEFAULT_PASSWORD


    def create_email(self) -> str:
        response = self.session.get(self.NEW_EMAIL_URL, headers=self.HEADERS)
        response.encoding = "utf-8-sig"
        return response.json().get("email")


    def register_email(self, email: str) -> None:
        payload = {
            "name": Faker("ja_JP").name(),
            "email": email,
            "password": self.password,
            "confirmPassword": self.password,
        }
        response = self.session.post(self.SIGNUP_URL, json=payload)
        
        if response.json().get("success", False):
            print(f"Registered {email}")
        else:
            print(f"Failed to register {email}")


    def get_messages(self) -> List:
        response = self.session.get(self.MESSAGES_URL, headers=self.HEADERS)
        response.encoding = "utf-8-sig"
        return response.json()


    def wait_messsage(self, attempt: int = 30) -> None:
        curr_attempt = 0

        while curr_attempt < attempt:
            print(f"Attempt: {curr_attempt}")
            messages = self.get_messages()

            if len(messages) > 1:
                print("Got a message")
                return

            print("Empty")
            curr_attempt += 1
            time.sleep(1)

    def activate_account(self) -> str:
        response = self.session.get(self.MESSAGE_URL)
        soup = BeautifulSoup(response.text, "lxml")
        activate_link = soup.select_one("td[valign=middle]>a").get("href")
        self.session.get(activate_link)
        print("Account activated")

    def create_key(self) -> str:
        response = self.session.post(self.NEW_KEY_URL, json={"name": ""})
        return response.json().get("key")

    def write_api_key(self, key: str) -> None:
        with open("api.key", "w") as file:
            file.write(key)

    def generate_api_key(self) -> str:
        email = self.create_email()
        print(f"Email: {email}")
        
        try:
            self.register_email(email)
            self.wait_messsage()
            self.activate_account()
            
            key = self.create_key()
        finally:
            self.session.close()
        
        self.write_api_key(key)
        return key
    

def generate_api_key() -> None:
    return GetimgReger().generate_api_key()


if __name__ == "__main__":
    generate_api_key()
