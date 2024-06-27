from typing import Mapping

import httpx

from . import pipelines
from ._base_client import SyncAPIClient


class GetimgAI(SyncAPIClient):
    controlnet: pipelines.ControlNet
    enhancement: pipelines.Enhancement
    id_adapter: pipelines.IDAdapter
    image_to_image: pipelines.ImageToImage
    inpainting: pipelines.Inpainting
    instruct: pipelines.Instruct
    models: pipelines.Models
    text_to_image: pipelines.TextToImage

    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("GETIMG_API_KEY")
        if api_key is None:
            raise NotImplementedError("Failed to get API Key")
        self.api_key = api_key

        if base_url is None:
            base_url = "https://api.getimg.ai/v1"

        super().__init__(
            base_url=base_url,
            timeout=timeout,
            custom_headers=custom_headers,
            http_client=http_client,
        )

        self.controlnet = pipelines.ControlNet(self)
        self.enhancement = pipelines.Enhancement(self)
        self.id_adapter = pipelines.IDAdapter(self)
        self.image_to_image = pipelines.ImageToImage(self)
        self.inpainting = pipelines.Inpainting(self)
        self.instruct = pipelines.Instruct(self)
        self.models = pipelines.Models(self)
        self.text_to_image = pipelines.TextToImage(self)

    @property
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    def default_headers(self) -> dict[str, str]:
        return {**super().default_headers, **self._custom_headers}


class AuthGetimgAI(SyncAPIClient):
    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        if not base_url:
            base_url = "https://api.getimg.ai/dashboard"

        super().__init__(
            base_url=base_url,
            timeout=timeout,
            custom_headers=custom_headers,
            http_client=http_client,
        )

    def signup(self, *, email: str, username: str, password: str) -> dict:
        payload = self._make_payload(locals())
        payload["confirmPassword"] = password
        return self.post("/me", json=payload).json()

    def signin(self, *, email: str, password: str) -> dict:
        return self.post("/auth", json=self._make_payload(locals())).json()

    def create_api_key(self, *, name: str = "") -> dict:
        return self.post("/keys", json=self._make_payload(locals())).json()


class TempMail(SyncAPIClient):
    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        if not base_url:
            base_url = "https://www.disposablemail.com"

        super().__init__(
            base_url=base_url,
            timeout=timeout,
            custom_headers=custom_headers,
            http_client=http_client,
        )

    def create_email(self) -> dict:
        return self.get("/index/index").json()

    def get_mailbox(self) -> dict:
        return self.get("/index/refresh").json()

    def get_message_content(self, message_id) -> str:
        return self.get(f"/email/id/{message_id}").text

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            **super().default_headers, 
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers,
        }

