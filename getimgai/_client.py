from typing import Optional, Union, Dict

import httpx
from httpx import Timeout, URL
from getimg_api_autoreg import autoreg_api_key

from . import resources
from ._base_client import SyncAPIClient
from .utils import _save_api_key, _load_api_key


class GetimgAI(SyncAPIClient):
    api_key: str

    models: resources.Models
    instruct: resources.Instruct
    idadapter: resources.IDAdapter
    controlnet: resources.ControlNet
    inpainting: resources.Inpainting
    enhancement: resources.Enhancement
    text_to_image: resources.TextToImage
    image_to_image: resources.ImageToImage

    base_url = "https://api.getimg.ai"

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        timeout: Optional[Union[float, Timeout]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(
            base_url=self.base_url,
            timeout=timeout,
            custom_headers=custom_headers,
            http_client=http_client,
        )
        if not api_key:
            api_key = _load_api_key()
        if not api_key:
            api_key = autoreg_api_key()
            _save_api_key(api_key)

        self.api_key = api_key

        self.models = resources.Models(self)
        self.instruct = resources.Instruct(self)
        self.idadapter = resources.IDAdapter(self)
        self.controlnet = resources.ControlNet(self)
        self.inpainting = resources.Inpainting(self)
        self.enhancement = resources.Enhancement(self)
        self.text_to_image = resources.TextToImage(self)
        self.image_to_image = resources.ImageToImage(self)

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    @property
    def default_headers(self) -> Dict[str, str]:
        return {**super().default_headers, **self._custom_headers}

