from typing import Optional, Dict

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

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        if not api_key:
            api_key = _load_api_key()
        if not api_key:
            api_key = autoreg_api_key()
            _save_api_key(api_key)

        self.api_key = api_key

        super().__init__(timeout=timeout)

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
