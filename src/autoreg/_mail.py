import re
from typing import TypeVar, Mapping, List, Any

import httpx

from ..clients import SyncAPIAuthMail


MailMessageT = TypeVar("Mal")


class AuthMail(SyncAPIAuthMail):
    _base_url = "https://www.disposablemail.com"
    _regex_verify = r'href="(https:\/\/u2293344[^"]+)'

    address: str

    def __init__(
        self,
        *,
        timeout: float | httpx.Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ):
        super().__init__(base_url=self._base_url,
                         timeout=timeout,
                         custom_headers=custom_headers,
                         http_client=http_client)

        email_data = self._client.create_email()
        self.address = email_data["email"]

    @property
    def default_headers(self) -> dict[str, str]:
        return {"X-Requested-With": "XMLHttpRequest"}

    @classmethod
    def _extract_verification_url(cls, content: str) -> str:
        match = re.search(cls._regex_verify, content, re.M)
        if match:
            return match.group(1)
        raise NotImplementedError("Failed to find verification url")

    @staticmethod
    def _find_verification_message(mailbox: List[MailMessageT]) -> MailMessageT:
        for message in mailbox:
            if "getimg.ai" in message.get("od"):
                return message
        return None

    @staticmethod
    def _find_keyword(keyword: str, mailbox: List[MailMessageT]) -> MailMessageT:
        if message := next(filter(lambda x: keyword in x["predmet"], mailbox), None):
            return message
        raise NotImplementedError("Failed to find keyword in mailbox")

    def create_email(self) -> httpx.Response:
        return self.get("/index/index")

    def get_mailbox(self) -> httpx.Response:
        return self.get("/index/refresh")

    def get_message_content(self, message_id) -> httpx.Response:
        return self.get(f"/email/id/{message_id}")

    def wait_message(
        self,
        *,
        keyword: str | None = None,
        attemps: int = 10,
        delay: float = 3,
    ) -> MailMessageT:
        while attemps > 0:
            mailbox = self.get_mailbox()
            if len(mailbox) > 1:
                if keyword:
                    return self._find_keyword(keyword, mailbox)
                return mailbox.pop(0)
            attemps -= 1
            time.sleep(delay)
        raise NotImplementedError("Failed to recieve verification message")

    def get_verification_url(self) -> str:
        print(self.address)
        message = cls.wait_message(keyword="getimg.ai")
        content = cls.get_message_content(message["id"])
        return cls._extract_verification_url(content)

