import re
import time
from typing import Mapping, TypeVar

import httpx

from ._paths import PATH_API_KEY
from ._utils import generate_string
from ._client import AuthGetimgAI, TempMail

MailMessageT = TypeVar("MailMessageT")


class RegerGetimgAI:
    _getimg_client: AuthGetimgAI
    _mail_client: TempMail

    email_address: str
    email_password: str

    _default_password = "zpqw8shwcs"
    _regex_verify = r'(https:\/\/u2293344[^"]+)'

    def __init__(self) -> None:
        self._getimg_client = AuthGetimgAI()
        self._mail_client = TempMail()

        email = self._mail_client.create_email()
        self.email_address = email["email"]

        print(self.email_address)

    def close(self) -> None:
        if hasattr(self, "_getimg_client"):
            self._getimg_client.close()
        if hasattr(self, "_mail_client"):
            self._mail_client.close()

    def __enter__(self) -> "RegerGetimgAI":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def get_verify_url(self) -> str:
        message = self._wait_message(keyword="getimg.ai")
        content = self._mail_client.get_message_content(message["id"])
        return self._extract_verify_url(content)

    def register_account(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        if not username:
            username = generate_string()
        if not password:
            self.email_password = self._default_password

        data = self._getimg_client.signup(
            email=self.email_address,
            username=username,
            password=self.email_password)

        if data.get("success", False) is False:
            raise NotImplementedError("Failed to create an account")

    def activate_account(self) -> None:
        verify_url = self.get_verify_url()
        if self._getimg_client.get(verify_url).status_code != 302:
            raise NotImplementedError("Failed to verify the account")

    def get_api_key(self) -> str:
        self.register_account()
        self.activate_account()
        self._getimg_client.signin(
            email=self.email_address,
            password=self.email_password)
        api_key = self._getimg_client.create_api_key()["key"]
        PATH_API_KEY.write_text(api_key)
        return api_key

    def _wait_message(
        self,
        *,
        keyword: str | None = None,
        attemps: int = 10,
        delay: float = 3,
    ) -> MailMessageT:
        while attemps > 0:
            mailbox = self._mail_client.get_mailbox()
            if len(mailbox) > 1:
                if keyword:
                    return self._find_keyword(keyword, mailbox)
                return mailbox.pop(0)
            attemps -= 1
            time.sleep(delay)
        raise NotImplementedError("Failed to recieve verify message")

    def _extract_verify_url(self, html_content: str) -> str:
        match = re.search(self._regex_verify, html_content, re.M)
        if match:
            return match.group(1)
        raise NotImplementedError("Failed to find verify url")

    def _find_verify_message(self, mailbox: list[MailMessageT]) -> MailMessageT:
        for message in mailbox:
            if "getimg.ai" in message.get("od"):
                return message
        return None

    def _find_keyword(self, keyword: str, mailbox: list[MailMessageT]) -> MailMessageT:
        if message := next(filter(lambda x: keyword in x["predmet"], mailbox), None):
            return message
        raise NotImplementedError("Failed to find keyword in mailbox")
