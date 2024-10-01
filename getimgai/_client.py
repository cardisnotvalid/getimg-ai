from . import resources
from ._base_client import SyncAPIClient


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

    def __init__(self, api_key, *, timeout=None):
        if not api_key:
            raise ValueError("api key was not passed")
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
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    def get_account_balance(self):
        return self.get("account/balance")
