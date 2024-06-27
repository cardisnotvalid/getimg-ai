from typing import Optional

from .temp_mail import TempMail
from ..client import AuthGetimg

from ..utils import generate_string
from ..paths import PATH_API_KEY


class GetImgReger:
    email: str
    username: str
    password: str

    def __init__(self, client: Optional[AuthGetimg] = None):
        self._client = client or AuthGetimg()
        self._temp_mail = TempMail()

        self.email = self._temp_mail.address

    def close(self):
        self._client.close()
        self._temp_mail.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def register_account(
        self,
        *,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        if not username:
            self.username = generate_string()
        if not password:
            self.password = generate_string()
        data = self._client.signup(self.email, self.username, self.password)

        if data.get("success", False) is False:
            raise NotImplementedError("Failed to create an account")

    def activate_account(self):
        verify_url = self._temp_mail.get_verification_url()

        response = self._client.get(verify_url)
        if response.status_code != 302:
            raise NotImplementedError("Failed to verify the account")

    def get_api_key(self):
        self.register_account()
        self.activate_account()
        self._client.signin(self.email, self.password)

        api_key = self._client.create_api_key().get("key")
        PATH_API_KEY.write_text(api_key)
        return api_key

